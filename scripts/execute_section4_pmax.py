import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
customer_neg_criterion_service = client.get_service('CustomerNegativeCriterionService')
campaign_service = client.get_service('CampaignService')
campaign_criterion_service = client.get_service('CampaignCriterionService')

customer_id = '9496728294'

def add_account_negative_keywords():
    print(">>> Setting up Account-level Negative Keywords...")
    keywords = ['ai', 'generator', 'chatgpt', 'bot', 'free api']
    ops = []
    for kw in keywords:
        op = client.get_type('CustomerNegativeCriterionOperation')
        criterion = op.create
        criterion.type_ = client.enums.CriterionTypeEnum.KEYWORD
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        ops.append(op)
    
    try:
        resp = customer_neg_criterion_service.mutate_customer_negative_criteria(customer_id=customer_id, operations=ops)
        print(f"Added {len(resp.results)} account-level negative keywords.")
    except Exception as e:
        print(f"Error adding account negative keywords: {e}")

def add_account_app_exclusions():
    print(">>> Setting up Account-level Mobile App Category Exclusions (All Apps)...")
    op = client.get_type('CustomerNegativeCriterionOperation')
    criterion = op.create
    criterion.type_ = client.enums.CriterionTypeEnum.MOBILE_APP_CATEGORY
    # 69500 is the constant ID for All Apps
    criterion.mobile_app_category.mobile_app_category_constant = "mobileAppCategoryConstants/69500"
    
    try:
        resp = customer_neg_criterion_service.mutate_customer_negative_criteria(customer_id=customer_id, operations=[op])
        print("Added account-level exclusion for ALL Mobile Apps.")
    except Exception as e:
        print(f"Error adding app exclusions (might already exist): {e}")

def update_pmax_campaigns():
    print(">>> Awaking PMax Campaigns and configuring settings...")
    query = """
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        WHERE campaign.name IN ('Google-PMax-Postman', 'Google-PMax-CP-Global')
    """
    stream = ga_service.search_stream(customer_id=customer_id, query=query)
    
    campaign_ops = []
    postman_campaign_id = None
    
    for batch in stream:
        for row in batch.results:
            op = client.get_type('CampaignOperation')
            campaign = op.update
            campaign.resource_name = campaign_service.campaign_path(customer_id, row.campaign.id)
            
            # Enable the campaign
            campaign.status = client.enums.CampaignStatusEnum.ENABLED
            op.update_mask.paths.append("status")
            
            if row.campaign.name == 'Google-PMax-Postman':
                postman_campaign_id = row.campaign.id
                
            print(f"Configuring {row.campaign.name}: ENABLED")
            campaign_ops.append(op)
            
    if campaign_ops:
        try:
            resp = campaign_service.mutate_campaigns(customer_id=customer_id, operations=campaign_ops)
            print(f"Successfully updated and ENABLED {len(resp.results)} PMax campaigns.")
        except Exception as e:
            print(f"Error updating PMax campaigns: {e}")
            
    return postman_campaign_id

def exclude_geos_for_postman(postman_campaign_id):
    if not postman_campaign_id:
        return
    print(f">>> Adding Geo Exclusions (US & UK) for Google-PMax-Postman (ID: {postman_campaign_id})...")
    # US = 2840, UK = 2826
    geos = ['2840', '2826']
    ops = []
    for geo in geos:
        op = client.get_type('CampaignCriterionOperation')
        criterion = op.create
        criterion.campaign = campaign_service.campaign_path(customer_id, postman_campaign_id)
        criterion.type_ = client.enums.CriterionTypeEnum.LOCATION
        criterion.location.geo_target_constant = f"geoTargetConstants/{geo}"
        criterion.negative = True
        ops.append(op)
        
    try:
        resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
        print(f"Successfully excluded {len(resp.results)} countries (US & UK) from Google-PMax-Postman.")
    except Exception as e:
        print(f"Error adding Geo Exclusions: {e}")

if __name__ == '__main__':
    postman_id = update_pmax_campaigns()
    exclude_geos_for_postman(postman_id)
    print(">>> Section 4 PMax Execution Completed!")
