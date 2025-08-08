import os, time

LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, "audit.log")

def _ensure_logs():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

def run(site="N/A", scope="N/A", **kwargs):
    """
    audit.start:
      site="Boise" scope="ISO-27001" -> append start event to logs/audit.log
    """
    _ensure_logs()
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | START | site={site} | scope={scope}"
    with open(LOG_PATH,"a",encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"[audit] {line}")
    return "Audit start logged."
