import os
import requests
import json
import datetime

# Configuration
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

METABASE_URL = "https://metabase.apifox.cn/"
METABASE_USERNAME = "bob@apifox.com"
METABASE_PASSWORD = "08103245981Zgh"

def query_metabase():
    print(">>> Logging into Metabase...")
    session_res = requests.post(f"{METABASE_URL}api/session", json={
        "username": METABASE_USERNAME, 
        "password": METABASE_PASSWORD
    })
    session_id = session_res.json().get("id")
    if not session_id:
        print(f"FAILED to login: {session_res.text}")
        return

    headers = {"X-Metabase-Session": session_id}
    
    # Query for last week (2026-04-13 to 2026-04-19)
    sql = """
    SELECT
      DATE(`user_trackings`.`created_at`) AS `date`,
      `user_trackings`.`utm_campaign` AS `campaign`,
      COUNT(*) AS `count`
    FROM
      `user_trackings`
    WHERE
      `user_trackings`.`created_at` >= '2026-04-13'
      AND `user_trackings`.`created_at` < '2026-04-20'
      AND (
        `user_trackings`.utm_source = 'google_search'
        OR `user_trackings`.utm_source = 'google_dsa'
      )
    GROUP BY
      DATE(`user_trackings`.`created_at`),
      `user_trackings`.`utm_campaign`
    ORDER BY
      `date` ASC,
      `count` DESC
    """
    
    print(">>> Fetching databases...")
    db_res = requests.get(f"{METABASE_URL}api/database", headers=headers)
    databases = db_res.json()
    if isinstance(databases, dict):
        databases = databases.get('data', [])
    
    db_id = None
    for db in databases:
        if db.get('name') == 'Apidog RDS':
            db_id = db['id']
            break
    if not db_id:
        db_id = databases[0]['id']

    print(f">>> Querying Metabase (DB ID: {db_id})...")
    query_payload = {
        "database": db_id,
        "type": "native",
        "native": {"query": sql},
        "parameters": []
    }
    
    res = requests.post(f"{METABASE_URL}api/dataset", json=query_payload, headers=headers)
    data = res.json()
    
    with open("query_results.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(">>> Results saved to query_results.json")

if __name__ == "__main__":
    query_metabase()
