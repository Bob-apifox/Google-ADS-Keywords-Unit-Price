import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

CONFIG = [
    {
        "comp": "Stoplight",
        "ag": "Compare-Best-Stoplight-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-stoplight/",
        "pitch": ["Full OpenAPI 3.1 Native", "100% Offline Mode", "1-Click Migration"]
    },
    {
        "comp": "Mintlify",
        "ag": "Compare-Best-Mintlify-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-mintlify/",
        "pitch": ["Auto-Generated Docs", "Live API Testing", "Smart Mocking in One"]
    },
    {
        "comp": "Readme.io",
        "ag": "Compare-Best-Readme-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-readme/",
        "pitch": ["No Per-Seat Markup", "Integrated Design Doc", "Test Suite Included"]
    },
    {
        "comp": "Insomnia",
        "ag": "Compare-Best-Insomnia-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-insomnia/",
        "pitch": ["No Mandatory Login", "Zero Execution Limits", "100% Offline Local Testing"]
    },
    {
        "comp": "Bruno",
        "ag": "Compare-Best-Bruno-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-bruno/",
        "pitch": ["Git-Native Local-First", "Full Visual UI", "Mock & Test Suite"]
    },
    {
        "comp": "Hoppscotch",
        "ag": "Compare-Best-Hoppscotch-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-hoppscotch/",
        "pitch": ["Native Desktop App", "Multi-Protocol Support", "Enterprise Ready API Tool"]
    },
    {
        "comp": "RapidAPI",
        "ag": "Compare-Best-RapidAPI-Alt-2026",
        "url": "https://apidog.com/compare/apidog-vs-rapidapi/",
        "pitch": ["100% Offline Privacy", "Enterprise SOC2 Compliance", "Migrate Without Hassle"]
    }
]

FINAL_URL_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def create_rsa_op(client, ag_res, url, pitch_texts, comp_name, var_index):
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
    h1_text = f"Top {comp_name} Alternative" if var_index == 1 else f"Best {comp_name} Alternative"
    h1.text = h1_text[:30]
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
    d2.text = f"Migrate seamlessly. Experience {pitch_texts[2]}."[:90]
    rsa.descriptions.append(d2)
    
    return op

def execute_section7_ads():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")
    aga_svc = client.get_service("AdGroupAdService")
    
    # Fetch AdGroup Resource Names
    ag_names = [item['ag'] for item in CONFIG]
    q_ag = "SELECT ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.name IN (" + ", ".join([f"'{ag}'" for ag in ag_names]) + ")"
    ag_res_map = {}
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            ag_res_map[row.ad_group.name] = row.ad_group.resource_name
            
    ad_ops = []
    
    for item in CONFIG:
        ag_name = item['ag']
        if ag_name not in ag_res_map:
            print(f"AdGroup {ag_name} not found.")
            continue
        ag_res = ag_res_map[ag_name]
        
        # Create 3 RSAs
        for i in range(3):
            ad_ops.append(create_rsa_op(client, ag_res, item['url'], item['pitch'], item['comp'], i))
            
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
        else:
             print("All ads uploaded successfully!")
                 
    print("[SUCCESS] Section 7 Ads Fixed!")

if __name__ == '__main__':
    execute_section7_ads()
