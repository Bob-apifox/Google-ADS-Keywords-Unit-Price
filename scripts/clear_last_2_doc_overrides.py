import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")

    q = """
        SELECT ad_group.id, ad_group.name, ad_group.resource_name
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-Doc-Global'
          AND ad_group.target_cpa_micros > 0
    """
    ops = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            ag_op = client.get_type("AdGroupOperation")
            ag = ag_op.update
            ag.resource_name = row.ad_group.resource_name
            client.copy_from(ag_op.update_mask, protobuf_helpers.field_mask(None, client.get_type("AdGroup")._pb))
            ag_op.update_mask.paths.append("target_cpa_micros")
            ops.append(ag_op)

    if ops:
        ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ops)
        print(f"Successfully cleared {len(ops)} overrides in Google-Sa-Doc-Global!")

if __name__ == '__main__':
    main()
