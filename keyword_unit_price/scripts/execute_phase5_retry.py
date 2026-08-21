import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.api_core.protobuf_helpers import field_mask

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

client = None
for i in range(3):
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        break
    except Exception as e:
        time.sleep(2)

if not client:
    print("Could not connect.")
    sys.exit(1)

def get_campaign_id(campaign_name):
    query = f"SELECT campaign.id FROM campaign WHERE campaign.name = '{campaign_name}' AND campaign.status = 'ENABLED'"
    ga_service = client.get_service("GoogleAdsService")
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    return row.campaign.id
        except:
            time.sleep(2)
    return None

def get_first_ad_group_id(campaign_id):
    query = f"SELECT ad_group.id FROM ad_group WHERE campaign.id = {campaign_id} AND ad_group.status = 'ENABLED' LIMIT 1"
    ga_service = client.get_service("GoogleAdsService")
    for _ in range(5):
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    return row.ad_group.id
        except:
            time.sleep(2)
    return None

def add_negative_keywords(campaign_name, keywords):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
        
    camp_crit_service = client.get_service("CampaignCriterionService")
    operations = []
    
    for kw in keywords:
        op = client.get_type("CampaignCriterionOperation")
        crit = op.create
        crit.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, camp_id)
        crit.negative = True
        crit.keyword.text = kw
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        operations.append(op)
        
    for _ in range(5):
        try:
            camp_crit_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Added negatives to {campaign_name}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to add negatives to {campaign_name}")

def add_expansion_keywords(campaign_name, keywords):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
    ag_id = get_first_ad_group_id(camp_id)
    if not ag_id: return
        
    ag_crit_service = client.get_service("AdGroupCriterionService")
    operations = []
    
    for kw in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        crit = op.create
        crit.ad_group = client.get_service("AdGroupService").ad_group_path(CUSTOMER_ID, ag_id)
        crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        crit.keyword.text = kw
        crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(op)
        
    for _ in range(5):
        try:
            ag_crit_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"✅ Added expansions to {campaign_name}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to add expansions to {campaign_name}")

def update_adgroup_cpa(campaign_name, new_cpa_micros):
    camp_id = get_campaign_id(campaign_name)
    if not camp_id: return
    ag_id = get_first_ad_group_id(camp_id)
    if not ag_id: return
    
    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.update
    ag.resource_name = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
    ag.target_cpa_micros = int(new_cpa_micros)
    
    client.copy_from(op.update_mask, field_mask(None, ag._pb))
    
    for _ in range(5):
        try:
            ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
            print(f"✅ Updated CPA for {campaign_name}")
            return
        except Exception:
            time.sleep(2)
    print(f"❌ Failed to update CPA for {campaign_name}")

def main():
    print("--- Retrying Failed Uploads ---")
    add_negative_keywords("Google-Sa-Doc-Global", ["api doc", "nanonets", "dogapi", "ai documentation generator", "nextdocs", "swaggerhub", "rest client"])
    add_expansion_keywords("Google-Sa-Fern-Global", ["fern api alternative", "fern api generator", "fern vs openapi"])
    update_adgroup_cpa("Google-Sa-Debug-Global", 1840000)

if __name__ == "__main__":
    main()
