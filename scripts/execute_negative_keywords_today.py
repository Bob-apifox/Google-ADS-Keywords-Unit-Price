import os
import sys
import re
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

plan_path = r"C:\Users\bobzh\.gemini\antigravity-ide\brain\df619394-c984-4a1b-a06e-a4f08016a39a\implementation_plan.md"

with open(plan_path, "r", encoding="utf-8") as f:
    content = f.read()

# Parse campaigns and their negative keywords
# Format: #### [MODIFY] Campaign: Google-Sa-Stoplight-Global
# - ➕ 添加精准否定词: `[web speech api]`
campaign_negatives = {}
current_campaign = None

for line in content.split("\n"):
    camp_match = re.search(r"#### \[MODIFY\] Campaign: (.*)", line)
    if camp_match:
        current_campaign = camp_match.group(1).strip()
        campaign_negatives[current_campaign] = []
        continue
    
    kw_match = re.search(r"➕ 添加精准否定词: `\[(.*?)\]`", line)
    if kw_match and current_campaign:
        kw = kw_match.group(1).strip()
        campaign_negatives[current_campaign].append(kw)

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_criterion_service = client.get_service('CampaignCriterionService')
customer_id = '9496728294'

# First, get campaign IDs for the required campaigns
q = "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status != 'REMOVED'"
stream = ga_service.search_stream(customer_id=customer_id, query=q)

camp_name_to_id = {}
for batch in stream:
    for row in batch.results:
        camp_name_to_id[row.campaign.name] = row.campaign.id

operations = []
for camp_name, kws in campaign_negatives.items():
    if not kws: continue
    
    if camp_name not in camp_name_to_id:
        print(f"Warning: Campaign {camp_name} not found.")
        continue
        
    camp_id = camp_name_to_id[camp_name]
    print(f"Campaign: {camp_name} (ID: {camp_id})")
    for kw in kws:
        print(f"  - Adding EXACT negative: [{kw}]")
        
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = ga_service.campaign_path(customer_id, camp_id)
        criterion.negative = True
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        
        operations.append(operation)

if operations:
    print(f"Mutating {len(operations)} negative keywords...")
    response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Successfully added {len(response.results)} negative keywords.")
else:
    print("No negative keywords found in the plan to add.")
