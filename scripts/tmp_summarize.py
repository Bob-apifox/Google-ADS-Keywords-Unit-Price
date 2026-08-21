import json
from collections import defaultdict

with open("query_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = data['data']['rows']
by_day = defaultdict(int)
by_campaign = defaultdict(int)
total = 0

for row in rows:
    date_str = row[0].split('T')[0]
    campaign = row[1]
    count = row[2]
    
    by_day[date_str] += count
    by_campaign[campaign] += count
    total += count

summary = {
    "total": total,
    "by_day": dict(sorted(by_day.items())),
    "top_campaigns": dict(sorted(by_campaign.items(), key=lambda x: x[1], reverse=True)[:10])
}

print(json.dumps(summary, indent=2))
