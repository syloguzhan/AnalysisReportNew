import os
import json
import time
from datetime import datetime, timedelta


REPORTS_DIR = "saved_reports"
os.makedirs(REPORTS_DIR,exist_ok=True)

def get_report_path(domain):
    filename = f"{domain}.json"
    return os.path.join(REPORTS_DIR,filename)


def save_report_to_file(domain,data):
    report_path = get_report_path(domain)
    wrapped_data = {
        "created_at" : datetime.utcnow().isoformat(),
        "report_data" : data
    }
    with open(report_path,"w", encoding="utf-8" ) as f:
        json.dump(wrapped_data, f, ensure_ascii=False, indent=2)


def load_report_if_recent(domain, max_age_days=7):
    start = time.time()
    report_path = get_report_path(domain)

    if not os.path.exists(report_path):
        return None

    with open(report_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    created_at = datetime.fromisoformat(content["created_at"])
    elapsed = time.time() - start

    if datetime.utcnow() - created_at <= timedelta(days=max_age_days):
        print(f">>> JSON LOAD + CHECK SÜRESİ: {elapsed:.2f} sn")
        return {
            "saved_at": content["created_at"],
            **content["report_data"]
        }

    print(f">>> Cache VAR ama süresi dolmuş. Süre: {elapsed:.2f} sn")
    return None






