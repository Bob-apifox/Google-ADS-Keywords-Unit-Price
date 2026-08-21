import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def get_google_ads_client():
    return GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)

def add_expansion_keywords_exact(client):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ag_service = client.get_service("AdGroupService")
    
    # Target Ad Groups
    targets = {
        ("Google-Sa-Solutions-API-First-Global", "Design-First Workflow"): [
            '"api first development platform"',
            '"api contract first design tool"',
            '"visual api design and mock tool"',
            '[api first design tool]'
        ],
        ("Google-Sa-DSA-Postman-Global", "Postman Alternative-DSA-Global"): [
            '"postman alternative open source"',
            '"best postman replacement for team"',
            '"lightweight postman alternative"'
        ]
    }
    
    # Query Ad Group IDs
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT campaign.name, ad_group.name, ad_group.id
        FROM ad_group
        WHERE campaign.status = 'ENABLED' AND ad_group.status = 'ENABLED'
    """
    ag_map = {}
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            ag_map[(row.campaign.name, row.ad_group.name)] = str(row.ad_group.id)
            
    operations = []
    for (c_name, ag_name), keywords in targets.items():
        if (c_name, ag_name) not in ag_map:
            print(f"⚠️ 无法在账户中找到广告组: [{c_name}] -> [{ag_name}]")
            continue
        ag_id = ag_map[(c_name, ag_name)]
        ag_resource = ag_service.ad_group_path(CUSTOMER_ID, ag_id)
        
        for kw in keywords:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_resource
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            
            if kw.startswith("[") and kw.endswith("]"):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                crit.keyword.text = kw[1:-1]
            elif kw.startswith('"') and kw.endswith('"'):
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw[1:-1]
            else:
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                crit.keyword.text = kw
            operations.append(op)
            
    if operations:
        req = client.get_type("MutateAdGroupCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(operations)
        req.partial_failure = True
        ag_criterion_service.mutate_ad_group_criteria(request=req)
        print(f"✅ 成功补全注入 {len(operations)} 个黄金拓展词至 [{list(targets.keys())}]！")

if __name__ == "__main__":
    client = get_google_ads_client()
    add_expansion_keywords_exact(client)
