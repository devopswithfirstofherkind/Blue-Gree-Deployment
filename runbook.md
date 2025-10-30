# 🧭 Runbook: Blue-Green Monitoring & Alert Response

## Alert Types

### 1️⃣ Failover Detected
**Meaning:** Traffic switched pools (e.g., Blue → Green).  
**Action:** Check health of the failed app. Run `curl /version` or inspect logs.

### 2️⃣ High Error Rate
**Meaning:** More than 2% of requests returned 5xx in the last 200 requests.  
**Action:** Inspect Nginx and app logs. Validate upstream health.

### 3️⃣ Recovery
**Meaning:** Traffic restored to the primary pool.  
**Action:** Resume monitoring.

## Suppress Alerts
Set `MAINTENANCE_MODE=true` in `.env` before planned toggles.
