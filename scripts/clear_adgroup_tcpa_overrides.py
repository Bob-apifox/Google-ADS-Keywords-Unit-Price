import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGET_CAMPAIGNS = [
    "Google-Sa-Stoplight-Global",
    "Google-Sa-Insomnia-Global",
    "Google-Sa-MCP-Infrastructure",
    "Google-Sa-Func-CICD-Global",
    "Google-Sa-Jmeter-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Solutions-AI-LLM-Global",
    "Google-Sa-Comp-HeavyQA-Global",
    "Google-Sa-Func-MultiProtocol-Global",
    "Google-Sa-DSA-Alternatives-Global"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")

    print("==========================================================================")
    print("[STARTING] Clearing Ad Group Level Target CPA Overrides (Revert to Campaign)")
    print("==========================================================================")

    names_str = ", ".join([f"'{n}'" for n in TARGET_CAMPAIGNS])
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
            ad_group.id,
            ad_group.name,
            ad_group.resource_name,
            ad_group.status,
            ad_group.target_cpa_micros
        FROM ad_group
        WHERE campaign.name IN ({names_str})
          AND ad_group.status != 'REMOVED'
          AND ad_group.target_cpa_micros > 0
    """

    ad_groups_to_clear = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            ad_groups_to_clear.append({
                'cname': row.campaign.name,
                'ag_name': row.ad_group.name,
                'ag_resource': row.ad_group.resource_name,
                'old_tcpa': row.ad_group.target_cpa_micros / 1000000.0
            })

    print(f"Found {len(ad_groups_to_clear)} Ad Groups with explicit tCPA overrides to clear.")

    operations = []
    for item in ad_groups_to_clear:
        ag_op = client.get_type("AdGroupOperation")
        ag = ag_op.update
        ag.resource_name = item['ag_resource']
        # In Google Ads API, clearing target_cpa_micros by omitting/clearing the field via field mask
        # Setting target_cpa_micros to None or using field mask with target_cpa_micros cleared:
        client.copy_from(ag_op.update_mask, protobuf_helpers.field_mask(None, client.get_type("AdGroup")._pb))
        # Add target_cpa_micros to update mask explicitly to clear it
        ag_op.update_mask.paths.append("target_cpa_micros")
        operations.append(ag_op)
        print(f"  └─ Clearing override on [{item['cname']}] -> Ad Group: {item['ag_name']} (Old override: ${item['old_tcpa']:.2f})")

    if operations:
        try:
            resp = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=operations)
            print(f"\n[SUCCESS] Successfully cleared overrides on {len(resp.results)} Ad Groups!")
        except Exception as e:
            print(f"\n[ERROR] Clearing overrides failed: {e}")
    else:
        print("\n[INFO] No Ad Group overrides found. All Ad Groups already inherit from Campaign.")

    print("\n==========================================================================")
    print("[FINISHED] Ad Group tCPA overrides cleared. All groups now inherit cleanly!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
