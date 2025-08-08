from datetime import datetime
import platform
import os

def run(**kwargs):
    """
    Minimal status command for Glenn.AI.
    Accepts optional kwargs like site=Boise quarter=Q3, but they’re optional.
    """
    site = kwargs.get("site", "N/A")
    quarter = kwargs.get("quarter", "N/A")

    info = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "cwd": os.getcwd(),
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()}",
        "site": site,
        "quarter": quarter,
        "message": "Glenn.AI router online; commands package reachable."
    }

    # Pretty-print to stdout, and also return a one-liner summary
    print("[status] System snapshot:")
    for k, v in info.items():
        print(f"  - {k}: {v}")

    return f"Status OK — {info['platform']} @ {info['time']}"
