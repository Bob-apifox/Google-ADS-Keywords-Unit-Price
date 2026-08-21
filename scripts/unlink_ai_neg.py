import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def unlink_ai_neg():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    camp_shared_set_service = client.get_service("CampaignSharedSetService")
    
    q = """
        SELECT campaign_shared_set.resource_name, campaign.name, shared_set.name 
        FROM campaign_shared_set 
        WHERE campaign.name = 'Google-Sa-Solutions-AI-LLM-Global' 
          AND shared_set.name = 'Negative-Global-AI-Isolation'
    """
    
    ops = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            print(f"Found link for Campaign: {row.campaign.name} & SharedSet: {row.shared_set.name}")
            op = client.get_type("CampaignSharedSetOperation")
            op.remove = row.campaign_shared_set.resource_name
            ops.append(op)
            
    if ops:
        print(f"Removing {len(ops)} CampaignSharedSet links...")
        req = client.get_type("MutateCampaignSharedSetsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        resp = camp_shared_set_service.mutate_campaign_shared_sets(request=req)
        for res in resp.results:
            print(f"Removed link: {res.resource_name}")
        print("[SUCCESS] AI Negative List successfully unlinked from AI Campaign!")
    else:
        print("No link found. It might have already been removed or not linked.")

if __name__ == '__main__':
    unlink_ai_neg()
