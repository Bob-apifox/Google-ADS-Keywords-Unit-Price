import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

CONFIG = [
    {
        "campaign": "Google-Sa-Postman-Global",
        "ad_group": "Postman Alternative-Global",
        "match_types": ["PHRASE", "EXACT"],
        "keywords": ["postman alternative tools", "alternativas a postman", "postman online testing"],
        "final_urls": ["https://apidog.com/compare/apidog-vs-postman/", "https://apidog.com/postman-alternative/"]
    },
    {
        "campaign": "Google-Sa-Postman-Global",
        "ad_group": "Enterprise-Compliance-Migration",
        "match_types": ["PHRASE"],
        "keywords": ["postman enterprise pricing", "postman enterprise limit"],
        "final_urls": ["https://apidog.com/postman-alternative/", "https://apidog.com/"]
    },
    {
        "campaign": "Google-Sa-Bruno-Global",
        "ad_group": "Bruno--Global",
        "match_types": ["EXACT"],
        "keywords": ["bruno api client", "bruno postman alternative"],
        "final_urls": ["https://apidog.com/compare/apidog-vs-bruno/"]
    },
    {
        "campaign": "Google-Sa-Hoppscotch-Global",
        "ad_group": "Hoppscotch--Global",
        "match_types": ["EXACT"],
        "keywords": ["hoppscotch alternative", "hoppscotch desktop app"],
        "final_urls": ["https://apidog.com/compare/apidog-vs-hoppscotch/"]
    },
    {
        "campaign": "Google-Sa-RapidAPI-Global",
        "ad_group": "RapidAPI--Global",
        "match_types": ["EXACT"],
        "keywords": ["rapidapi alternative", "rapidapi vs postman"],
        "final_urls": ["https://apidog.com/compare/apidog-vs-rapidapi/"]
    },
    {
        "campaign": "Google-Sa-Comp-VSCode-Global",
        "ad_group": "Thunder-Client",
        "match_types": ["PHRASE", "EXACT"],
        "keywords": ["thunder client download", "thunderclient"],
        "final_urls": ["https://apidog.com/extension/"]
    },
    {
        "campaign": "Google-Sa-Insomnia-Global",
        "ad_group": "Insomnia api-Global",
        "match_types": ["PHRASE"],
        "keywords": ["insomnia tool", "insomnia rest client download"],
        "final_urls": ["https://apidog.com/insomnia-alternative/"]
    },
    {
        "campaign": "Google-Sa-Swagger-Global",
        "ad_group": "Swagger Docs-Global",
        "match_types": ["PHRASE"],
        "keywords": ["swagger ui generator", "swagger ui alternative"],
        "final_urls": ["https://apidog.com/api-doc/"]
    },
    {
        "campaign": "Google-Sa-Solutions-AI-LLM-Global",
        "ad_group": "AI-Code-Generation",
        "match_types": ["PHRASE", "EXACT"],
        "keywords": ["anythingllm", "magic loops api", "ai api testing online"],
        "final_urls": ["https://apidog.com/ai-powered-workflow/"]
    }
]

def execute_section2():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    agbc_service = client.get_service('AdGroupCriterionService')
    
    # 1. Fetch Campaign Match Types
    camp_match_map = {}
    q_camp = "SELECT campaign.name, campaign.keyword_match_type FROM campaign WHERE campaign.status = 'ENABLED'"
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            # 4 == BROAD
            camp_match_map[row.campaign.name] = (row.campaign.keyword_match_type.name == 'BROAD')
            
    # 2. Fetch AdGroup IDs
    ag_map = {}
    q_ag = """
        SELECT ad_group.id, ad_group.name, campaign.name 
        FROM ad_group 
        WHERE ad_group.status = 'ENABLED' 
          AND campaign.status = 'ENABLED'
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            key = f"{row.campaign.name}|{row.ad_group.name.lower()}"
            ag_map[key] = row.ad_group.id

    ops = []
    
    for item in CONFIG:
        c_name = item['campaign']
        ag_name = item['ad_group']
        key = f"{c_name}|{ag_name.lower()}"
        
        if key not in ag_map:
            print(f"WARNING: Could not find AdGroup '{ag_name}' in Campaign '{c_name}'. Skipping.")
            continue
            
        ag_id = ag_map[key]
        ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        
        is_broad_only = camp_match_map.get(c_name, False)
        
        for kw in item['keywords']:
            for m_type in item['match_types']:
                op = client.get_type('AdGroupCriterionOperation')
                agc = op.create
                agc.ad_group = ag_path
                agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                
                agc.keyword.text = kw
                
                if is_broad_only:
                    agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
                else:
                    if m_type == "PHRASE":
                        agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                    elif m_type == "EXACT":
                        agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                    
                # Add Keyword Final URLs
                agc.final_urls.extend(item['final_urls'])
                
                ops.append(op)
                
    if ops:
        print(f"Uploading {len(ops)} keywords with Final URLs (accounting for Broad Match Only rules)...")
        for i in range(0, len(ops), 100):
            req = client.get_type('MutateAdGroupCriteriaRequest')
            req.customer_id = CUSTOMER_ID
            req.operations.extend(ops[i:i+100])
            req.partial_failure = True
            resp = agbc_service.mutate_ad_group_criteria(request=req)
            
            if resp.partial_failure_error and resp.partial_failure_error.details:
                for err in resp.partial_failure_error.details:
                    print(f"Keyword Upload Error: {err}")
            else:
                print(f"Batch uploaded successfully.")
                
        print("[SUCCESS] Section 2 Keywords and Final URLs injected successfully!")
    else:
        print("No operations to execute.")

if __name__ == '__main__':
    execute_section2()
