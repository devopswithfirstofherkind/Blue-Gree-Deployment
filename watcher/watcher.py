import os, time, json, requests, re
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
    print("Sending Slack alert:", msg)
    try:
        requests.post(SLACK_WEBHOOK_URL, json={"text": msg})
    except Exception as e:
        print("Slack error:", e)

def monitor():
    global last_alert_time, last_pool
    print("Starting log watcher...")
    with open(LOG_PATH, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            # Use regex to find fields like pool=..., upstream_status=...
            pool_match = re.search(r"pool=(\S+)", line)
            status_match = re.search(r"upstream_status=(\d+)", line)

            pool = pool_match.group(1) if pool_match else "-"
            status = status_match.group(1) if status_match else "-"

            print(f"Read line | pool={pool}, status={status}")

            if status.startswith("5"):
                errors.append(1)
            else:
                errors.append(0)

            # Error rate check
            if len(errors) >= 10:  # Avoid noise until we have some samples
                rate = (sum(errors) / len(errors)) * 100
                now = time.time()
                if rate > ERROR_RATE_THRESHOLD and now - last_alert_time > ALERT_COOLDOWN_SEC:
                    send_slack(f":rotating_light: High error rate detected ({rate:.2f}%) in {pool} pool")
                    last_alert_time = now

            # Failover check
            if last_pool and pool != last_pool and pool != "-":
                send_slack(f":repeat: Failover detected! {last_pool} → {pool}")
                last_alert_time = time.time()

            last_pool = pool

if __name__ == "__main__":
    monitor()
