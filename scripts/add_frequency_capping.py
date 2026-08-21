import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

CAMPAIGN_IDS = [24126382470, 24131994659]

def add_frequency_capping(client, customer_id):
    campaign_service = client.get_service("CampaignService")
    ops = []
    for cid in CAMPAIGN_IDS:
        op = client.get_type("CampaignOperation")
        c = op.update
        c.resource_name = f"customers/{customer_id}/campaigns/{cid}"

        # Set frequency cap: 4 impressions per day per user
        cap = client.get_type("FrequencyCapEntry")
        cap.key.level = client.enums.FrequencyCapLevelEnum.AD_GROUP
        cap.key.event_type = client.enums.FrequencyCapEventTypeEnum.IMPRESSION
        cap.key.time_unit = client.enums.FrequencyCapTimeUnitEnum.DAY
        cap.key.time_length = 1
        cap.cap = 4
        c.frequency_caps.append(cap)

        client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, c._pb))
        ops.append(op)

    try:
        campaign_service.mutate_campaigns(customer_id=customer_id, operations=ops)
        print("[SUCCESS] Added Frequency Capping (Max 4 impressions/day/user) to both Display campaigns!")
    except Exception as e:
        print(f"[NOTE] Frequency cap update: {e}")

if __name__ == '__main__':
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    add_frequency_capping(client, CUSTOMER_ID)
