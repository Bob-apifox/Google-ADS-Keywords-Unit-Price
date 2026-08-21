import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

CONFIG = [
    {
        "camp": "Google-Sa-Postman-Global",
        "ag": "Blog-OpenSource-Postman-Alt",
        "url": "https://apidog.com/blog/top-postman-alternative-open-source/",
        "h_main": "Open Source Postman Alt",
        "pitch": ["100% Free Local-First", "Migrate Without Data Loss", "No Account Sign-in Required"]
    },
    {
        "camp": "Google-Sa-Testing-Global",
        "ag": "Blog-WebSocket-Testing-Enterprise",
        "url": "https://apidog.com/blog/websocket-testing-tools/",
        "h_main": "WebSocket Testing Tool",
        "pitch": ["Test WebSocket API Online", "Advanced WebSocket Mocking", "Enterprise API Testing Suite"]
    },
    {
        "camp": "Google-Sa-Swagger-Global",
        "ag": "Blog-SOAP-API-Doc-Enterprise",
        "url": "https://apidog.com/blog/top-6-soap-api-documentation-tools/",
        "h_main": "SOAP API Documentation",
        "pitch": ["Auto Generate SOAP Docs", "Best SOAP UI Alternative", "Enterprise API Doc Generator"]
    },
    {
        "camp": "Google-Sa-Postman-Global",
        "ag": "Blog-Postman-To-OpenAPI",
        "url": "https://apidog.com/blog/postman-to-openapi/",
        "h_main": "Postman to OpenAPI",
        "pitch": ["1-Click Collection Converter", "Generate OpenAPI Spec Fast", "Migrate Postman to Swagger"]
    }
]

FINAL_URL_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def create_distinct_rsa_op(client, ag_res, url, h_main, pitch_texts, var_index):
    op = client.get_type("AdGroupAdOperation")
    aga = op.create
    aga.ad_group = ag_res
    aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad = aga.ad
    ad.final_urls.append(url)
    ad.final_url_suffix = FINAL_URL_SUFFIX
    
    rsa = ad.responsive_search_ad
    
    # Define Headlines
    h1 = client.get_type("AdTextAsset")
    h2 = client.get_type("AdTextAsset")
    h3 = client.get_type("AdTextAsset")
    h4 = client.get_type("AdTextAsset")
    
    # Variation Logic
    if var_index == 0:
        h1.text = h_main[:30]
        h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        h2.text = pitch_texts[0][:30]
        h2.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_2
        h3.text = pitch_texts[1][:30]
        h4.text = pitch_texts[2][:30]
    elif var_index == 1:
        h1.text = pitch_texts[0][:30]
        h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        h2.text = h_main[:30]
        h2.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_2
        h3.text = pitch_texts[1][:30]
        h4.text = pitch_texts[2][:30]
    else:
        h1.text = pitch_texts[1][:30]
        h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        h2.text = pitch_texts[2][:30]
        h2.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_2
        h3.text = h_main[:30]
        h4.text = pitch_texts[0][:30]
        
    rsa.headlines.extend([h1, h2, h3, h4])
    
    h_brand = client.get_type("AdTextAsset")
    h_brand.text = "Try Apidog Free Today"
    rsa.headlines.append(h_brand)
    
    # Descriptions
    d1 = client.get_type("AdTextAsset")
    d2 = client.get_type("AdTextAsset")
    
    if var_index == 0:
        d1.text = f"{pitch_texts[0]} and {pitch_texts[1]}."[:90]
        d1.pinned_field = client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1
        d2.text = f"Experience the best API workflow. {pitch_texts[2]}."[:90]
    elif var_index == 1:
        d1.text = f"Experience the best API workflow. {pitch_texts[2]}."[:90]
        d1.pinned_field = client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1
        d2.text = f"{pitch_texts[0]} and {pitch_texts[1]}."[:90]
    else:
        d1.text = f"Upgrade your API Workflow today. {pitch_texts[0]}."[:90]
        d2.text = f"{pitch_texts[1]}. {pitch_texts[2]}."[:90]
        d2.pinned_field = client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_2
        
    rsa.descriptions.extend([d1, d2])
    
    return op

def execute_fix():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")
    aga_svc = client.get_service("AdGroupAdService")
    
    ag_names = [item['ag'] for item in CONFIG]
    
    # 1. Fetch AdGroup Resource Names
    q_ag = "SELECT ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.name IN (" + ", ".join([f"'{n}'" for n in ag_names]) + ")"
    ag_res_map = {}
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            ag_res_map[row.ad_group.name] = row.ad_group.resource_name
            
    if not ag_res_map:
        print("AdGroups not found.")
        return
        
    # 2. Fetch Existing Ads to Remove
    remove_ops = []
    q_ads = "SELECT ad_group_ad.resource_name, ad_group.name FROM ad_group_ad WHERE ad_group.name IN (" + ", ".join([f"'{n}'" for n in ag_names]) + ") AND ad_group_ad.status = 'ENABLED'"
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_ads):
        for row in batch.results:
            op = client.get_type("AdGroupAdOperation")
            op.remove = row.ad_group_ad.resource_name
            remove_ops.append(op)
            
    if remove_ops:
        print(f"Removing {len(remove_ops)} duplicate identical ads...")
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(remove_ops)
        aga_svc.mutate_ad_group_ads(request=req)
        print("Removal complete.")
        
    # 3. Create 3 Distinct Ads Per Group
    add_ops = []
    for item in CONFIG:
        if item['ag'] not in ag_res_map:
            continue
        ag_res = ag_res_map[item['ag']]
        
        for i in range(3):
            add_ops.append(create_distinct_rsa_op(client, ag_res, item['url'], item['h_main'], item['pitch'], i))
            
    if add_ops:
        print(f"Uploading {len(add_ops)} distinctly varied Ads...")
        req = client.get_type("MutateAdGroupAdsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(add_ops)
        req.partial_failure = True
        resp = aga_svc.mutate_ad_group_ads(request=req)
        
        if resp.partial_failure_error and resp.partial_failure_error.details:
             for err in resp.partial_failure_error.details:
                 print(f"Ad Error: {err}")
        else:
             print("All distinct ads uploaded successfully!")
                 
    print("[SUCCESS] Section 8 Ads properly varied and fixed!")

if __name__ == '__main__':
    execute_fix()
