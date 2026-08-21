import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
campaign_criterion_service = client.get_service('CampaignCriterionService')
ad_group_service = client.get_service('AdGroupService')
ad_group_criterion_service = client.get_service('AdGroupCriterionService')

# 1. Add Negative Keywords to both DSA campaigns
dsa_campaigns = {
    'Google-Sa-DSA-Global': '22062217351',
    'Google-Sa-DSA-Postman-Global': '22058259794'
}
negative_words = ['javascript', 'react', 'docker', 'shadcn', 'glm 5.2', 'glm', 'user testing', 'css', 'html', 'vue']

criterion_ops = []
for c_name, c_id in dsa_campaigns.items():
    for word in negative_words:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id)
        criterion.negative = True
        criterion.keyword.text = word
        # Using exact match to avoid blocking relevant long tail
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        criterion_ops.append(op)

print("Executing Negative Keywords Injection for DSA...")
try:
    response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=criterion_ops)
    print(f"Success: Added {len(response.results)} negative keywords to DSA campaigns.")
except Exception as e:
    print(f"Error: {e}")

# 2. Create the new Competitor-VS-DSA Ad Group in Google-Sa-DSA-Global
c_id_global = dsa_campaigns['Google-Sa-DSA-Global']

print("Creating Competitor-VS-DSA Ad Group...")
op = client.get_type("AdGroupOperation")
ad_group = op.create
ad_group.name = "Competitor-VS-DSA-Global"
ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
ad_group.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id_global)
ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
# set cpc bid to $2.00 (2000000 micros)
ad_group.cpc_bid_micros = 2000000

try:
    ag_response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
    new_ag_resource = ag_response.results[0].resource_name
    print(f"Success: Created Ad Group {new_ag_resource}")
    
    # 3. Create Webpage Criteria
    vs_targets = ['postman', 'insomnia', 'stoplight', 'swagger', 'bruno', 'readme']
    
    agc_ops = []
    for target in vs_targets:
        agc_op = client.get_type("AdGroupCriterionOperation")
        agc = agc_op.create
        agc.ad_group = new_ag_resource
        agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        
        # Set Webpage Info
        webpage_info = agc.webpage
        webpage_info.criterion_name = f"VS {target.capitalize()}"
        
        condition = client.get_type("WebpageConditionInfo")
        condition.operand = client.enums.WebpageConditionOperandEnum.URL
        condition.operator = client.enums.WebpageConditionOperatorEnum.CONTAINS
        condition.argument = f"/vs-{target}"
        
        webpage_info.conditions.append(condition)
        agc_ops.append(agc_op)
        
    try:
        agc_response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=agc_ops)
        print(f"Success: Created {len(agc_response.results)} Webpage Criteria for VS pages.")
    except Exception as e:
        print(f"Error creating webpage criteria: {e}")
        
except Exception as e:
    print(f"Error creating ad group: {e}")

print("DONE.")
