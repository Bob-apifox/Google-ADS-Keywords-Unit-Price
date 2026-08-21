import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

CONFIG = [
    {
        "comp": "Stoplight",
        "camp": "Google-Sa-Stoplight-Global",
        "ag": "Compare-Best-Stoplight-Alt-2026",
        "kws": ["best stoplight alternative", "top stoplight alternatives", "stoplight vs apidog", "why migrate from stoplight"],
        "url": "https://apidog.com/compare/apidog-vs-stoplight/",
        "pitch": ["Full OpenAPI 3.1 Native", "100% Offline Mode", "1-Click Migration"]
    },
    {
        "comp": "Mintlify",
        "camp": "Google-Sa-Mintlify-Global",
        "ag": "Compare-Best-Mintlify-Alt-2026",
        "kws": ["best mintlify alternative", "top mintlify alternatives", "mintlify vs apidog", "mintlify api docs alternative"],
        "url": "https://apidog.com/compare/apidog-vs-mintlify/",
        "pitch": ["Auto-Generated Docs", "Live API Testing", "Smart Mocking in One"]
    },
    {
        "comp": "Readme.io",
        "camp": "Google-Sa-Readme-Global",
        "ag": "Compare-Best-Readme-Alt-2026",
        "kws": ["best readme io alternative", "top readme alternatives", "readme vs apidog", "readme api documentation alternative"],
        "url": "https://apidog.com/compare/apidog-vs-readme/",
        "pitch": ["No Per-Seat Markup", "Integrated Design Doc", "Test Suite Included"]
    },
    {
        "comp": "Insomnia",
        "camp": "Google-Sa-Insomnia-Global",
        "ag": "Compare-Best-Insomnia-Alt-2026",
        "kws": ["best insomnia alternative", "top insomnia alternatives", "insomnia vs apidog", "insomnia rest client alternative"],
        "url": "https://apidog.com/compare/apidog-vs-insomnia/",
        "pitch": ["No Mandatory Account Sign-in", "Zero Runner Execution Limits", "100% Offline Local Testing"]
    },
    {
        "comp": "Bruno",
        "camp": "Google-Sa-Bruno-Global",
        "ag": "Compare-Best-Bruno-Alt-2026",
        "kws": ["best bruno alternative", "top bruno alternatives", "bruno vs apidog", "bruno postman alternative"],
        "url": "https://apidog.com/compare/apidog-vs-bruno/",
        "pitch": ["Git-Native Local-First", "Full Visual UI", "Mock & Test Suite"]
    },
    {
        "comp": "Hoppscotch",
        "camp": "Google-Sa-Hoppscotch-Global",
        "ag": "Compare-Best-Hoppscotch-Alt-2026",
        "kws": ["best hoppscotch alternative", "top hoppscotch alternatives", "hoppscotch vs apidog", "hoppscotch desktop app alternative"],
        "url": "https://apidog.com/compare/apidog-vs-hoppscotch/",
        "pitch": ["Native Desktop Performance", "Advanced Multi-Protocol Support", "Enterprise Ready API Tool"]
    },
    {
        "comp": "RapidAPI",
        "camp": "Google-Sa-RapidAPI-Global",
        "ag": "Compare-Best-RapidAPI-Alt-2026",
        "kws": ["best rapidapi alternative", "top rapidapi alternatives", "rapidapi vs apidog", "rapidapi client alternative"],
        "url": "https://apidog.com/compare/apidog-vs-rapidapi/",
        "pitch": ["100% Offline Privacy", "Enterprise SOC2 Compliance", "Migrate Without Hassle"]
    }
]

FINAL_URL_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
TARGET_CPA = 1500000

def create_rsa_op(client, ag_res, url, pitch_texts, var_index):
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
    h1.text = f"Top {pitch_texts[0][:15]} Alternative" if var_index == 1 else f"Best Alternative Tool"
    h1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    rsa.headlines.append(h1)
    
    for pt in pitch_texts:
        h = client.get_type("AdTextAsset")
        h.text = pt[:30] # Limit 30
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

def execute_section7():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")
    ag_svc = client.get_service("AdGroupService")
    agc_svc = client.get_service("AdGroupCriterionService")
    aga_svc = client.get_service("AdGroupAdService")
    
    # 1. Check Broad Match Only campaigns
    camp_map = {}
    camp_match = {}
    q_camp = "SELECT campaign.id, campaign.name, campaign.resource_name, campaign.keyword_match_type FROM campaign WHERE campaign.status = 'ENABLED'"
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            camp_map[row.campaign.name] = row.campaign.resource_name
            camp_match[row.campaign.name] = (row.campaign.keyword_match_type.name == 'BROAD')
            
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
        ag.target_cpa_micros = TARGET_CPA
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
                
        # 3 RSAs
        for i in range(3):
            ad_ops.append(create_rsa_op(client, ag_res, item['url'], item['pitch'], i))
            
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
                 
    print("[SUCCESS] Section 7 Content Compare Campaign Setup Complete!")

if __name__ == '__main__':
    execute_section7()
