import os
import sys
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.type,
            ad_group.status
        FROM ad_group
        WHERE campaign.status = 'ENABLED'
          AND ad_group.status != 'REMOVED'
        ORDER BY campaign.name, ad_group.name
    """

    print("=== Existing Campaigns and Ad Groups in Account ===")
    campaign_ag_map = {}
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                ag_name = row.ad_group.name
                ag_id = row.ad_group.id
                ag_type = row.ad_group.type_.name
                ag_status = row.ad_group.status.name
                
                if c_name not in campaign_ag_map:
                    campaign_ag_map[c_name] = []
                campaign_ag_map[c_name].append({
                    "id": ag_id,
                    "name": ag_name,
                    "type": ag_type,
                    "status": ag_status
                })

        for c_name, ag_list in campaign_ag_map.items():
            print(f"\n📂 Campaign: {c_name}")
            for ag in ag_list:
                print(f"   └── Ad Group: [{ag['id']}] {ag['name']} ({ag['type']}, {ag['status']})")

    except Exception as e:
        print(f"Error fetching ad groups: {e}")

if __name__ == "__main__":
    main()
