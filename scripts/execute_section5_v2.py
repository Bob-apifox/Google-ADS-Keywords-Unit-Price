import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
CAMPAIGN_NAME = 'Google-Sa-DSA-Global'

def execute_section5():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    budget_service = client.get_service('CampaignBudgetService')
    ag_service = client.get_service('AdGroupService')
    agc_service = client.get_service('AdGroupCriterionService')
    camp_crit_service = client.get_service('CampaignCriterionService')

    # 1. Fetch Campaign and Budget ID
    q_camp = f"SELECT campaign.id, campaign.resource_name, campaign.campaign_budget FROM campaign WHERE campaign.name = '{CAMPAIGN_NAME}' AND campaign.status = 'ENABLED'"
    camp_id = None
    camp_res = None
    budget_res = None
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            camp_id = row.campaign.id
            camp_res = row.campaign.resource_name
            budget_res = row.campaign.campaign_budget
            
    if not camp_id:
        print(f"Could not find active campaign: {CAMPAIGN_NAME}")
        return

    # 2. Increase Budget by 40%
    q_budget = f"SELECT campaign_budget.amount_micros FROM campaign_budget WHERE campaign_budget.resource_name = '{budget_res}'"
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_budget):
        for row in batch.results:
            current_micros = row.campaign_budget.amount_micros
            new_micros = int(current_micros * 1.4)
            print(f"Increasing budget from {current_micros/1000000} to {new_micros/1000000}")
            
            op = client.get_type("CampaignBudgetOperation")
            op.update.resource_name = budget_res
            op.update.amount_micros = new_micros
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, op.update._pb))
            budget_service.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])

    # 3. Create New Ad Groups with Target CPA of $2.31
    new_groups = ['DSA-Group-Postman-Alt-Blogs', 'DSA-Group-Enterprise-Tech']
    ag_ops = []
    for g in new_groups:
        op = client.get_type("AdGroupOperation")
        ag = op.create
        ag.campaign = camp_res
        ag.name = g
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
        # Set Target CPA for Ad Group to 2310000 micros ($2.31)
        ag.target_cpa_micros = 2310000
        ag_ops.append(op)
        
    print(f"Creating {len(new_groups)} new DSA AdGroups with CPA $2.31...")
    ag_resp = ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ag_ops)
    ag_res_map = {}
    for i, res in enumerate(ag_resp.results):
        print(f"Created AdGroup: {new_groups[i]} ({res.resource_name})")
        ag_res_map[new_groups[i]] = res.resource_name

    # 4. Inject URLs into Existing and New Groups
    mock_ag_res = None
    q_mock = f"SELECT ad_group.resource_name FROM ad_group WHERE campaign.id = {camp_id} AND ad_group.name = 'DSA-Mock-Group' AND ad_group.status = 'ENABLED'"
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_mock):
        for row in batch.results:
            mock_ag_res = row.ad_group.resource_name
            break
            
    url_injections = {
        'DSA-Group-Postman-Alt-Blogs': ['top-postman-alternative-open-source', 'postman-to-openapi'],
        'DSA-Group-Enterprise-Tech': ['websocket-testing-tools', 'top-6-soap-api-documentation-tools']
    }
    
    agc_ops = []
    
    def create_webpage_op(ad_group_res, url_contains):
        op = client.get_type("AdGroupCriterionOperation")
        agc = op.create
        agc.ad_group = ad_group_res
        agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        
        info = client.get_type("WebpageInfo")
        cond = client.get_type("WebpageConditionInfo")
        cond.operand = client.enums.WebpageConditionOperandEnum.URL
        cond.operator = client.enums.WebpageConditionOperatorEnum.CONTAINS
        cond.argument = url_contains
        
        info.conditions.append(cond)
        info.criterion_name = f"Target: {url_contains}"
        agc.webpage = info
        return op
        
    if mock_ag_res:
        agc_ops.append(create_webpage_op(mock_ag_res, '/api-debug/'))
    else:
        print("Warning: DSA-Mock-Group not found.")
        
    for g_name, urls in url_injections.items():
        if g_name in ag_res_map:
            ag_res = ag_res_map[g_name]
            for u in urls:
                agc_ops.append(create_webpage_op(ag_res, u))
                
    if agc_ops:
        print(f"Creating {len(agc_ops)} AdGroup Webpage Criteria...")
        req = client.get_type("MutateAdGroupCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(agc_ops)
        req.partial_failure = True
        agc_resp = agc_service.mutate_ad_group_criteria(request=req)
        if agc_resp.partial_failure_error and agc_resp.partial_failure_error.details:
             for err in agc_resp.partial_failure_error.details:
                 print(f"Error creating Webpage Criterion: {err}")
        else:
             print("Webpage criteria created successfully.")

    # 5. Global Campaign Exclusions
    exclusions = ['what-is', 'basics', 'tutorial', 'privacy', 'terms', 'login']
    camp_crit_ops = []
    for ex in exclusions:
        op = client.get_type("CampaignCriterionOperation")
        cc = op.create
        cc.campaign = camp_res
        cc.negative = True
        
        info = client.get_type("WebpageInfo")
        cond = client.get_type("WebpageConditionInfo")
        cond.operand = client.enums.WebpageConditionOperandEnum.URL
        cond.operator = client.enums.WebpageConditionOperatorEnum.CONTAINS
        cond.argument = ex
        
        info.conditions.append(cond)
        info.criterion_name = f"Exclude: {ex}"
        cc.webpage = info
        camp_crit_ops.append(op)
        
    if camp_crit_ops:
        print(f"Creating {len(camp_crit_ops)} Campaign Exclusions...")
        req = client.get_type("MutateCampaignCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(camp_crit_ops)
        req.partial_failure = True
        cc_resp = camp_crit_service.mutate_campaign_criteria(request=req)
        if cc_resp.partial_failure_error and cc_resp.partial_failure_error.details:
            for err in cc_resp.partial_failure_error.details:
                print(f"Error creating exclusion: {err}")
        else:
            print("Exclusions created successfully.")
            
    print("[SUCCESS] Section 5 DSA execution complete.")

if __name__ == '__main__':
    execute_section5()
