# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try: sys.stdout.reconfigure(encoding='utf-8')
except: pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

geo_mapping = {
    "Google-Sa-CP-AR": [2682, 2784, 2818, 2112, 2048, 2275, 2368, 2400, 2414, 2422, 2434, 2478, 2504, 2512, 2634, 2788], # Arabic countries
    "Google-Sa-CP-ESP-2": [2724, 2484, 2170, 2032, 2152, 2604], # TR renamed to ESP-2
    "Google-Sa-CP-JP": [2392],
    "Google-Sa-CP-KR": [2410],
    "Google-Sa-CP-VN": [2704],
    "Google-Sa-CP-ID": [2360],
    "Google-Sa-CP-TW": [2158],
    "Google-Sa-CP-DE": [2276, 2040, 2756], # DE, AT, CH
    "Google-Sa-CP-FR": [2250, 2056, 2124], # FR, BE, CA (some FR parts)
    "Google-Sa-CP-PT": [2620, 2076], # PT, BR
    "Google-Sa-CP-ES": [2724, 2484, 2170, 2032, 2152, 2604], # Original ES just in case
    "Google-Sa-CP-MX": [2724, 2484, 2170, 2032, 2152, 2604] # Original MX just in case
}

def execute_part1():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    campaign_service = client.get_service('CampaignService')
    campaign_criterion_service = client.get_service('CampaignCriterionService')
    ad_group_service = client.get_service('AdGroupService')
    
    # 1. Fetch campaigns and clear existing Geo criteria
    q_camp = """
        SELECT campaign.id, campaign.name, campaign.status, campaign.campaign_budget
        FROM campaign
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND campaign.status != 'REMOVED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp)
    
    camp_ops = []
    budget_ops = [] # We need to update budget objects directly if they are shared, but here we can just update campaign.campaign_budget
    budget_service = client.get_service('CampaignBudgetService')
    
    c_ids_to_clean = {}
    
    print(">>> Phase 1: Campaigns & Budgets")
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            c_id = row.campaign.id
            b_id = row.campaign.campaign_budget.split('/')[-1] if row.campaign.campaign_budget else None
            
            op = client.get_type('CampaignOperation')
            campaign = op.update
            campaign.resource_name = ga_service.campaign_path(CUSTOMER_ID, c_id)
            
            if c_name == 'Google-Sa-CP-ar':
                print(f"Pausing {c_name}...")
                campaign.status = client.enums.CampaignStatusEnum.PAUSED
                op.update_mask.paths.append("status")
                camp_ops.append(op)
                continue
                
            if c_name == 'Google-Sa-CP-TR':
                print(f"Renaming TR to ESP-2...")
                c_name = 'Google-Sa-CP-ESP-2'
                campaign.name = c_name
                op.update_mask.paths.append("name")
                
            if c_name in geo_mapping or "AR" in c_name or "JP" in c_name or "PT" in c_name or "FR" in c_name or "DE" in c_name or "ID" in c_name or "VN" in c_name or "KR" in c_name or "TW" in c_name:
                c_ids_to_clean[c_name] = c_id
                
                # We need to update Budget
                if b_id:
                    b_op = client.get_type('CampaignBudgetOperation')
                    budget = b_op.update
                    budget.resource_name = budget_service.campaign_budget_path(CUSTOMER_ID, b_id)
                    budget.amount_micros = 20000000 # $20
                    b_op.update_mask.paths.append("amount_micros")
                    budget_ops.append(b_op)
                    
            if op.update_mask.paths:
                camp_ops.append(op)

    # 2. Clear Existing Geo Criteria
    print(">>> Phase 2: Clearing old Geo Targets")
    q_geo = """
        SELECT campaign.id, campaign.name, campaign_criterion.criterion_id
        FROM campaign_criterion
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND campaign_criterion.type = 'LOCATION'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_geo)
    geo_remove_ops = []
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            if c_name in c_ids_to_clean or c_name == 'Google-Sa-CP-TR':
                op = client.get_type('CampaignCriterionOperation')
                op.remove = campaign_criterion_service.campaign_criterion_path(CUSTOMER_ID, row.campaign.id, row.campaign_criterion.criterion_id)
                geo_remove_ops.append(op)

    # 3. Add New Geo Criteria
    print(">>> Phase 3: Adding new Geo Targets")
    geo_add_ops = []
    for c_name, c_id in c_ids_to_clean.items():
        if c_name in geo_mapping:
            for geo_id in geo_mapping[c_name]:
                op = client.get_type('CampaignCriterionOperation')
                criterion = op.create
                criterion.campaign = ga_service.campaign_path(CUSTOMER_ID, c_id)
                criterion.location.geo_target_constant = client.get_service('GeoTargetConstantService').geo_target_constant_path(str(geo_id))
                geo_add_ops.append(op)
                
    # 4. Update AdGroup CPAs
    print(">>> Phase 4: Updating Postman AdGroup Target CPA")
    q_ag = """
        SELECT ad_group.id, ad_group.name, ad_group.status, campaign.name
        FROM ad_group
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag)
    ag_ops = []
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            if 'postman' in ag_name.lower() and c_name != 'Google-Sa-CP-ar':
                op = client.get_type('AdGroupOperation')
                ag = op.update
                ag.resource_name = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)
                ag.target_cpa_micros = 1500000 # $1.5
                ag.cpc_bid_micros = 1500000 # also set cpc bid limit just in case
                op.update_mask.paths.append("target_cpa_micros")
                op.update_mask.paths.append("cpc_bid_micros")
                ag_ops.append(op)

    # Execute all
    print(f"Executing {len(camp_ops)} campaign updates...")
    if camp_ops:
        req = client.get_type('MutateCampaignsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(camp_ops)
        req.partial_failure = True
        resp = campaign_service.mutate_campaigns(request=req)
        
    print(f"Executing {len(budget_ops)} budget updates...")
    if budget_ops:
        req = client.get_type('MutateCampaignBudgetsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(budget_ops)
        req.partial_failure = True
        resp = budget_service.mutate_campaign_budgets(request=req)

    print(f"Executing {len(geo_remove_ops)} geo removals...")
    if geo_remove_ops:
        # chunks of 2000
        for i in range(0, len(geo_remove_ops), 2000):
            req = client.get_type('MutateCampaignCriteriaRequest')
            req.customer_id = CUSTOMER_ID
            req.operations.extend(geo_remove_ops[i:i+2000])
            req.partial_failure = True
            campaign_criterion_service.mutate_campaign_criteria(request=req)
            
    print(f"Executing {len(geo_add_ops)} geo additions...")
    if geo_add_ops:
        # chunks of 2000
        for i in range(0, len(geo_add_ops), 2000):
            req = client.get_type('MutateCampaignCriteriaRequest')
            req.customer_id = CUSTOMER_ID
            req.operations.extend(geo_add_ops[i:i+2000])
            req.partial_failure = True
            campaign_criterion_service.mutate_campaign_criteria(request=req)
            
    print(f"Executing {len(ag_ops)} AdGroup CPA updates...")
    if ag_ops:
        req = client.get_type('MutateAdGroupsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ag_ops)
        req.partial_failure = True
        resp = ad_group_service.mutate_ad_groups(request=req)
        
    print("[SUCCESS] Part 1 Execution Finished!")
    return True

def main():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            if execute_part1():
                break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == '__main__':
    main()
