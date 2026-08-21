import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

TARGET_CPA = 1500000

AG_NAMES = [
    "Blog-OpenSource-Postman-Alt",
    "Blog-WebSocket-Testing-Enterprise",
    "Blog-SOAP-API-Doc-Enterprise",
    "Blog-Postman-To-OpenAPI"
]

def update_ag_cpa():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga = client.get_service("GoogleAdsService")
    ag_svc = client.get_service("AdGroupService")
    
    q_ag = "SELECT ad_group.name, ad_group.resource_name FROM ad_group WHERE ad_group.name IN (" + ", ".join([f"'{n}'" for n in AG_NAMES]) + ")"
    
    ops = []
    for batch in ga.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
        for row in batch.results:
            op = client.get_type("AdGroupOperation")
            op.update.resource_name = row.ad_group.resource_name
            op.update.target_cpa_micros = TARGET_CPA
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, op.update._pb))
            ops.append(op)
            
    if ops:
        print(f"Updating CPA for {len(ops)} Ad Groups to $1.50...")
        req = client.get_type("MutateAdGroupsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        resp = ag_svc.mutate_ad_groups(request=req)
        print("Update complete!")
    else:
        print("No Ad Groups found.")

if __name__ == '__main__':
    update_ag_cpa()
