import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

CONFIG = [
    {
        "camp": "Google-Sa-Postman-Global",
        "ag": "Blog-OpenSource-Postman-Alt",
        "kws": ["open source postman alternative", "free postman alternative open source", "postman open source replace"],
        "url": "https://apidog.com/blog/top-postman-alternative-open-source/",
        "h_main": "Open Source Postman Alt",
        "pitch": ["100% Free Local-First", "Migrate Without Data Loss", "No Account Sign-in Required"]
    },
    {
        "camp": "Google-Sa-Testing-Global",
        "ag": "Blog-WebSocket-Testing-Enterprise",
        "kws": ["websocket testing tool", "test websocket api online", "websocket mock server"],
        "url": "https://apidog.com/blog/websocket-testing-tools/",
        "h_main": "WebSocket Testing Tool",
        "pitch": ["Test WebSocket API Online", "Advanced WebSocket Mocking", "Enterprise API Testing Suite"]
    },
    {
        "camp": "Google-Sa-Swagger-Global",
        "ag": "Blog-SOAP-API-Doc-Enterprise",
        "kws": ["soap api documentation tool", "soap ui alternative", "generate soap docs"],
        "url": "https://apidog.com/blog/top-6-soap-api-documentation-tools/",
        "h_main": "SOAP API Documentation",
        "pitch": ["Auto Generate SOAP Docs", "Best SOAP UI Alternative", "Enterprise API Doc Generator"]
    },
    {
        "camp": "Google-Sa-Postman-Global",
        "ag": "Blog-Postman-To-OpenAPI",
        "kws": ["postman to openapi", "convert postman collection to swagger", "postman openapi generator"],
        "url": "https://apidog.com/blog/postman-to-openapi/",
        "h_main": "Postman to OpenAPI",
        "pitch": ["1-Click Collection Converter", "Generate OpenAPI Spec Fast", "Migrate Postman to Swagger"]
    }
]

FINAL_URL_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def create_rsa_op(client, ag_res, url, h_main, pitch_texts):
    op = client.get_type("AdGroupAdOperation")
    aga = op.create
    aga.ad_group = ag_res
    aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad = aga.ad
    ad.final_urls.append(url)
    ad.final_url_suffix = FINAL_URL_SUFFIX
    
    rsa = ad.responsive_search_ad
    
    # Headlines
    h1 = client.get_type("AdTextAsset")
    h1.text = h_main[:30]
    h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    rsa.headlines.append(h1)
    
    for pt in pitch_texts:
        h = client.get_type("AdTextAsset")
        h.text = pt[:30] 
        rsa.headlines.append(h)
        
    h_brand = client.get_type("AdTextAsset")
    h_brand.text = "Try Apidog Free Today"
    rsa.headlines.append(h_brand)
    
    # Descriptions
    d1 = client.get_type("AdTextAsset")
    d1.text = f"{pitch_texts[0]} and {pitch_texts[1]}."[:90]
    rsa.descriptions.append(d1)
    
    d2 = client.get_type("AdTextAsset")
    d2.text = f"Experience the best API workflow. {pitch_texts[2]}."[:90]
    rsa.descriptions.append(d2)
    
    return op

def execute_section8():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")
    ag_svc = client.get_service("AdGroupService")
    agc_svc = client.get_service("AdGroupCriterionService")
    aga_svc = client.get_service("AdGroupAdService")
    budget_svc = client.get_service("CampaignBudgetService")
    
    # 1. Fetch Campaigns, Budgets and Broad Match Settings
    camp_map = {}
    camp_match = {}
    q_camp = "SELECT campaign.id, campaign.name, campaign.resource_name, campaign.keyword_match_type, campaign.campaign_budget FROM campaign WHERE campaign.status = 'ENABLED'"
    
    postman_budget_res = None
    
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            c_name = row.campaign.name
            camp_map[c_name] = row.campaign.resource_name
            camp_match[c_name] = (row.campaign.keyword_match_type.name == 'BROAD')
            if c_name == 'Google-Sa-Postman-Global':
                postman_budget_res = row.campaign.campaign_budget
                
    # Increase Postman Campaign Budget by +50%
    if postman_budget_res:
        q_budget = f"SELECT campaign_budget.amount_micros FROM campaign_budget WHERE campaign_budget.resource_name = '{postman_budget_res}'"
        for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_budget):
            for row in batch.results:
                curr = row.campaign_budget.amount_micros
                new_b = int(curr * 1.5)
                op = client.get_type("CampaignBudgetOperation")
                op.update.resource_name = postman_budget_res
                op.update.amount_micros = new_b
                client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, op.update._pb))
                print(f"Increasing Postman Budget from {curr/1000000} to {new_b/1000000}")
                budget_svc.mutate_campaign_budgets(customer_id=CUSTOMER_ID, operations=[op])

    # 2. Create AdGroups
    ag_ops = []
    for item in CONFIG:
        if item['camp'] not in camp_map:
            print(f"Skipping {item['ag']}: Campaign {item['camp']} not found.")
            continue
        op = client.get_type("AdGroupOperation")
        ag = op.create
        ag.campaign = camp_map[item['camp']]
        ag.name = item['ag']
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag_ops.append(op)
        
    ag_res_map = {}
    if ag_ops:
        print(f"Creating {len(ag_ops)} Ad Groups...")
        resp = ag_svc.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ag_ops)
        for i, res in enumerate(resp.results):
            ag_name = ag_ops[i].create.name
            ag_res_map[ag_name] = res.resource_name
            
    # 3. Create Keywords and Ads
    kw_ops = []
    ad_ops = []
    
    for item in CONFIG:
        ag_name = item['ag']
        if ag_name not in ag_res_map:
            continue
        ag_res = ag_res_map[ag_name]
        is_broad = camp_match.get(item['camp'], False)
        
        # Keywords
        for kw in item['kws']:
            for mt in (['BROAD'] if is_broad else ['PHRASE', 'EXACT']):
                op = client.get_type("AdGroupCriterionOperation")
                agc = op.create
                agc.ad_group = ag_res
                agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                agc.keyword.text = kw
                if mt == 'BROAD':
                    agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
                elif mt == 'PHRASE':
                    agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                else:
                    agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                agc.final_urls.append(item['url'])
                kw_ops.append(op)
                
        # Create 3 RSAs
        for i in range(3):
            ad_ops.append(create_rsa_op(client, ag_res, item['url'], item['h_main'], item['pitch']))
            
    # Execute Keywords
    if kw_ops:
        print(f"Uploading {len(kw_ops)} Keywords...")
        req = client.get_type("MutateAdGroupCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(kw_ops)
        req.partial_failure = True
        resp = agc_svc.mutate_ad_group_criteria(request=req)
        if resp.partial_failure_error and resp.partial_failure_error.details:
             for err in resp.partial_failure_error.details:
                 print(f"Keyword Error: {err}")
                 
    # Execute Ads
    if ad_ops:
        print(f"Uploading {len(ad_ops)} Ads...")
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ad_ops)
        req.partial_failure = True
        resp = aga_svc.mutate_ad_group_ads(request=req)
        if resp.partial_failure_error and resp.partial_failure_error.details:
             for err in resp.partial_failure_error.details:
                 print(f"Ad Error: {err}")
                 
    print("[SUCCESS] Section 8 Execution Complete!")

if __name__ == '__main__':
    execute_section8()
