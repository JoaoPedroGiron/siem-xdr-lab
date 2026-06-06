#!/usr/bin/env python3
import requests
import time
import yaml
import logging
import hashlib
from datetime import datetime, timezone, timedelta

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

def load_config(path="/opt/wazuh-alert-bot/config.yaml"):
    with open(path) as f:
        return yaml.safe_load(f)

def get_alerts_from_indexer(cfg):
    try:
        now = datetime.now(timezone.utc)
        since = (now - timedelta(seconds=cfg['poll_interval'] + 10)).strftime('%Y-%m-%dT%H:%M:%SZ')
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"range": {"@timestamp": {"gte": since}}},
                        {"range": {"rule.level": {"gte": cfg['min_alert_level']}}}
                    ]
                }
            },
            "sort": [{"@timestamp": {"order": "desc"}}],
            "size": 50
        }
        # Correção aqui: índice wazuh-alerts-4.x-*
        r = requests.post(
            f"https://192.168.1.103:9200/wazuh-alerts-4.x-*/_search",
            json=query,
            auth=("admin", "SecretPassword"),
            verify=False,
            timeout=15
        )
        if r.status_code == 200:
            hits = r.json().get("hits", {}).get("hits", [])
            return [h["_source"] for h in hits]
    except Exception as e:
        log.error(f"Erro ao buscar alertas: {e}")
    return []

def send_slack(webhook_url, alert):
    rule = alert.get("rule", {})
    agent = alert.get("agent", {})
    level = rule.get("level", 0)
    severity = "CRITICO" if level >= 13 else ("ALTO" if level >= 10 else "MEDIO")
    color = "#FF0000" if level >= 13 else ("#FF8C00" if level >= 10 else "#FFD700")
    
    payload = {
        "attachments": [{
            "color": color,
            "title": f"WAZUH ALERT - {severity} (Nivel {level})",
            "text": rule.get("description", "N/A"),
            "fields": [
                {"title": "Agente", "value": f"{agent.get('name', 'N/A')}", "short": True},
                {"title": "Rule ID", "value": str(rule.get("id", "N/A")), "short": True}
            ]
        }]
    }
    return requests.post(webhook_url, json=payload, timeout=10).status_code == 200

def main():
    cfg = load_config()["wazuh"]
    webhook = load_config()["notifications"]["slack_webhook_url"]
    seen = set()
    while True:
        try:
            for alert in get_alerts_from_indexer(cfg):
                alert_id = hashlib.md5(f"{alert.get('@timestamp')}{alert.get('id')}".encode()).hexdigest()
                if alert_id not in seen:
                    seen.add(alert_id)
                    send_slack(webhook, alert)
        except Exception as e: log.error(f"Erro: {e}")
        time.sleep(cfg["poll_interval"])

if __name__ == "__main__": main()
