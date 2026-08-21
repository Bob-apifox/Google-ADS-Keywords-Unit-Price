import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
campaign_service = client.get_service("CampaignService")

campaign_id = '22286394432' # Google-Sa-CP-ROW-MultiLang
new_tcpa_micros = 3000000 # $3.00

print(f"Updating Campaign {campaign_id} Target CPA to $3.00...")

campaign_operation = client.get_type("CampaignOperation")
campaign = campaign_operation.update
campaign.resource_name = campaign_service.campaign_path(CUSTOMER_ID, campaign_id)
campaign.maximize_conversions.target_cpa_micros = new_tcpa_micros

client.copy_from(campaign_operation.update_mask, protobuf_helpers.field_mask(None, campaign._pb))

try:
    response = campaign_service.mutate_campaigns(
        customer_id=CUSTOMER_ID, operations=[campaign_operation]
    )
    print(f"Success! Updated Campaign: {response.results[0].resource_name}")
except Exception as e:
    print(f"Error updating campaign: {e}")
