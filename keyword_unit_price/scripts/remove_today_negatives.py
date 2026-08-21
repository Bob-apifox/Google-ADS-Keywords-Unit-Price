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

def remove_recent_negatives(client):
    ga_service = client.get_service("GoogleAdsService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    
    # 查找刚才注入的否定词文本列表
    target_negatives = [
        "api doc generator free", "swagger editor online", "postman online tool",
        "postman download windows 10", "postman desktop app free",
        "vscode download", "visual studio code online editor",
        "soapui tutorial pdf", "readyapi crack download",
        "fern openapi tutorial", "sdk generator python free",
        "apidog vs insomnia comparison", "apidog free account limit"
    ]
    
    query = """
        SELECT campaign_criterion.resource_name, campaign_criterion.keyword.text, campaign.name
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'KEYWORD'
          AND campaign_criterion.negative = TRUE
    """
    
    ops = []
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    for batch in stream:
        for row in batch.results:
            kw_text = row.campaign_criterion.keyword.text.lower().strip()
            res_name = row.campaign_criterion.resource_name
            if kw_text in [t.lower() for t in target_negatives]:
                op = client.get_type("CampaignCriterionOperation")
                op.remove = res_name
                ops.append(op)
                print(f"🗑️ 准备移除否定词: [{kw_text}] 来自系列 [{row.campaign.name}]")
                
    if ops:
        req = client.get_type("MutateCampaignCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        req.partial_failure = True
        campaign_criterion_service.mutate_campaign_criteria(request=req)
        print(f"✅ 成功移除 {len(ops)} 个今日新加的否定词！否定词计划已全量撤销。")
    else:
        print("ℹ️ 未查找到需要移除的今日否定词。")

if __name__ == "__main__":
    client = get_google_ads_client()
    remove_recent_negatives(client)
