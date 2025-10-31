import os, time, json, requests
from collections import deque

LOG_PATH = "/var/log/nginx/access.log"
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ERROR_RATE_THRESHOLD = float(os.getenv("ERROR_RATE_THRESHOLD", 2.0))
WINDOW_SIZE = int(os.getenv("WINDOW_SIZE", 200))
ALERT_COOLDOWN_SEC = int(os.getenv("ALERT_COOLDOWN_SEC", 300))

errors = deque(maxlen=WINDOW_SIZE)
last_alert_time = 0
last_pool = None

def send_slack(msg):
    if not SLACK_WEBHOOK_URL:
        print("No webhook configured.")
        return
    requests.post(SLACK_WEBHOOK_URL, json={"text": msg})

def monitor():
    global last_alert_time, last_pool
    with open(LOG_PATH, "r", errors="ignore") as f:
        f.seek(0, os.SEEK_END)  # safer version
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            parts = {kv.split("=")[0]: kv.split("=")[1] for kv in line.split() if "=" in kv}
            pool = parts.get("pool")
            status = parts.get("upstream_status", "")
            
            if status.startswith("5"):
                errors.append(1)
            else:
                errors.append(0)
            
            # Error rate check
            rate = (sum(errors)/len(errors))*100
            now = time.time()
            if rate > ERROR_RATE_THRESHOLD and now - last_alert_time > ALERT_COOLDOWN_SEC:
                send_slack(f":rotating_light: High error rate detected ({rate:.2f}%) in {pool} pool")
                last_alert_time = now
            
            # Failover check
            if last_pool and pool != last_pool:
                send_slack(f":repeat: Failover detected! {last_pool} → {pool}")
                last_alert_time = now
            last_pool = pool

if __name__ == "__main__":
    print("Starting log watcher...")
    monitor()
