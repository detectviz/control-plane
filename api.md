# Control-Plane 調用 SRE Assistant 的規格書建議

- 草稿用了一個統一入口 `POST /execute`，透過 `user_query` + `context` 包裝不同場景；
- 建議是針對常見場景（事件分析、報告、容量、summary）定義明確的 REST path，以保持語義清晰與可維護性。
- 把這些只讀 API 條列成一個「最小可用集合 (MVP Read-only API Set)」，在 Control-plane 先實作幾個最常用的。
- 最終需要整理成一份 **OpenAPI 3.1 YAML 草稿**，可以直接放進 Control-plane 與 SRE-assistant 專案裡做 Mock Server 測試

## 端點選項 A、B 策略是 **同時設計，但使用上有所分工**

- **短期 → `/execute` 是探索引擎**
- **長期 → `/diagnostics/*` 是產品接口**

### 如何使用

1.  **開發早期 / 探索階段**：
    - 優先用 `/execute`，降低摩擦，快速疊代功能。
2.  **功能成熟 / 固定化後**：
    - 將高頻使用的 `/execute` 調用抽象成對應的專用 API，例如 `/diagnostics/deployment`。
    - Control-plane 前端直接呼叫專用 API，不再組裝複雜的 `user_query`。
3.  **長期運行**：
    - `/execute` 保留作為後門（面向工程師、實驗功能、debugging）。
    - `/diagnostics/*`、`/summaries/*` 成為產品化 API，支撐 UI 與自動化流程。

### 端點選項總覽

- **統一入口 `/execute`**
    - 保持高度彈性，對應 ad-hoc、快速新增的診斷類問題。
    - `user_query` + `context`，交由 SRE-assistant 解讀。
- **高頻固定場景**（提供語義化 API，降低耦合度）：
    - `POST /diagnostics/deployment`
    - `POST /diagnostics/dashboard`
    - `POST /diagnostics/alerts`
    - `POST /summaries/daily`（dashboard 24h 小結）
    - `POST /capacity/analyze`
- **Control-plane 提供的只讀 API**（給 SRE-assistant 當 tools）：
    - `/api/v1/audit-logs`
    - `/api/v1/logs/:id`
    - `/api/v1/executions/:id`
    - `/api/v1/incidents?service=checkout`
    - （未來可擴展 /metrics, /incidents）

---

### 端點選項 A：`/execute`

- 定位：**統一入口**（Generic Agent API）。
- 適用場景：
    - Ad-hoc 查詢（用戶直接輸入自然語言）。
    - 尚未 productize 的需求（原型測試、快速迭代）。
    - 支援多種 Trigger Source（Dashboard UI、CLI、API）。
- 優勢：彈性高、擴展快、不需頻繁調整 API 定義。
- 缺點：上下文語意依賴 `user_query`，開發者與前端需維護 payload 模板。

### 端點選項 B：語義化 API，例如 `/diagnostics/deployment`

- 定位：**固定場景專用 API**（Productized Endpoint）。
- 適用場景：
    - 高頻業務流程（例如部署診斷、告警診斷、每日小結）。
    - Control-plane 前端有固定 UI 元件需要綁定。
    - 要做 RBAC、審計、SLA 保證的場景。
- 優勢：語義明確、payload 結構化、易於測試與治理。
- 缺點：每增加一種場景，就需要同步調整 API Spec 與實作。

## 第一部分：**主動 API**（Control-plane → SRE-assistant）：下達目標與任務

採用 **兩層 API 設計**：

1.  **統一入口** `/execute`（保持彈性，方便處理新需求或 ad-hoc query）。
2.  **語義化子端點**（適合高頻場景，減少 payload 模糊性與 client-side 模板化負擔）。

---

### 1.1 部署後健康分析

- **端點選項 A（通用入口）：**  
    `POST /execute`
- **端點選項 B（語義化）：**  
    `POST /diagnostics/deployment`

**Payload 範例**

```json
{
  "user_query": "Investigate deployment failure for service 'payment-api' in namespace 'production'.",
  "context": {
    "trigger_source": "ControlPlane::DeploymentMonitor",
    "service_name": "payment-api",
    "namespace": "production",
    "deployment_id": "deploy-xyz-12345",
    "image_tag": "v1.2.1"
  }
}
```

### 1.2 互動式儀表板診斷

- **端點選項 A：** `/execute`
- **端點選項 B：** `/diagnostics/dashboard`

**Payload 範例**

```json
{
  "user_query": "Why did p99 latency spike in the last 30 minutes?",
  "context": {
    "trigger_source": "ControlPlane::DashboardUI",
    "user_id": "user-abc-789",
    "service_name": "user-profile-svc",
    "namespace": "staging",
    "time_range": {
      "start": "2025-09-01T08:30:00Z",
      "end": "2025-09-01T09:00:00Z"
    }
  }
}
```

**回應建議支援 streaming**（WebSocket 或 SSE），因為這類交互更像「逐步推理」。

### 1.3 告警觸發診斷

- **端點選項 A：** `/execute`
- **端點選項 B：** `/diagnostics/alerts`

**Payload 範例**

```json
{
  "user_query": "Alert 'HighErrorRate' is firing for service 'checkout-svc'. Please investigate.",
  "context": {
    "trigger_source": "PrometheusAlertmanager",
    "alert_name": "HighErrorRate",
    "service_name": "checkout-svc",
    "summary": "The checkout service is experiencing an error rate over 5%.",
    "grafana_link": "http://grafana.example.com/d/..."
  }
}
```

**回應策略**：SRE-assistant 可以選擇直接回傳給 Control-plane，或透過自己的 Notification tool（Slack, Teams）下發。

## 第二部分：**只讀 API**（SRE-assistant → Control-plane）：拉取背景數據，支撐推理與決策。

這部分的 API 本質上是 **「資料供應器」**，讓 SRE-assistant 在做診斷或產生小結時，不需要 Control-plane 主動推送所有資料，而是能夠 **自己拉取需要的上下文**。

---

### 用途與價值

#### 1. 降低耦合

- 如果 Control-plane 每次都要把所有細節資料打包丟給 SRE-assistant，兩邊都會變得臃腫。
- 提供只讀 API，SRE-assistant 可以用「工具 (Tool)」的方式自己查詢，符合 Agent 自主決策的設計哲學。

#### 2. 支援自主推理

- 當 SRE-assistant 收到指令「調查過去 24 小時錯誤率異常」時，它可能需要：
    - 最近的 **變更紀錄**（audit logs）
    - 當時的 **事件或告警內容**
    - **執行紀錄**（例如 rollout logs）
- 這些資料透過 API 讓它自行調用，而不是 Control-plane 先猜測要給什麼。

#### 3. 可重褹用

- 這些 API 不只服務 SRE-assistant，還能給：
    - CLI 工具
    - 其他外部分析服務
    - 對接 AI Agent Framework（LangChain Tool、ADK Tool）
- 形成「平台化」的數據層，而不是點對點整合。

### 常見的只讀 API 類型

1.  **變更歷史 (Audit Logs)**
    - Endpoint: `GET /api/v1/audit-logs`
    - Query: `service_name`, `namespace?`, `start_time`, `end_time`
    - Response: JSON array of change events
    - 查詢服務的部署、配置變更，回答「最近誰動了什麼？」

2.  **執行紀錄 (Executions / Rollouts)**
    - Endpoint: `GET /api/v1/executions/:id`
    - 提供 rollout 歷史、pipeline log，讓 SRE-assistant 能驗證是否 rollback。

3.  **事件與告警 (Incidents / Alerts)**
    - Endpoint: `GET /api/v1/incidents?service=checkout`
    - 讓診斷能知道過去有沒有相關事故。

4.  **系統日誌 (Logs)**
    - Endpoint: `GET /api/v1/logs/:id`
    - 支援細節調查，例如「錯誤率升高」後去查應用 Log。

### 流程範例

1.  Control-plane 下達指令：
    ```json
    {
      "task": "generate_summary",
      "scope": "24h",
      "context": { "target": "dashboard_overview" }
    }
    ```
2.  SRE-assistant 開始工作 → 呼叫 Control-plane 提供的 API：
    ```http
    GET /api/v1/audit-logs?service_name=checkout-svc&start_time=...&end_time=...
    ```
3.  Control-plane 回傳 JSON → SRE-assistant 整合數據、判斷異常 → 回報摘要。
