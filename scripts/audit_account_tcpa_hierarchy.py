import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    q = """
        SELECT
            campaign.name,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
            ad_group.id,
            ad_group.name,
            ad_group.target_cpa_micros,
            ad_group.effective_target_cpa_micros,
            ad_group.effective_target_cpa_source
        FROM ad_group
        WHERE ad_group.status = 'ENABLED'
          AND campaign.status = 'ENABLED'
          AND campaign.name IN (
            'Google-Sa-CP-Global',
            'Google-Sa-Postman-Global',
            'Google-Sa-DSA-Alternatives-Global',
            'Google-Sa-Comp-HeavyQA-Global',
            'Google-Sa-Func-MultiProtocol-Global',
            'Google-Sa-Category-Competitor-Global',
            'Google-Sa-CP-TW',
            'Google-PMax-CP-Global',
            'Google-PMax-Postman',
            'Google-Sa-Solutions-AI-LLM-Global',
            'Google-Sa-Stoplight-Global',
            'Google-Sa-Insomnia-Global',
            'Google-Sa-MCP-Infrastructure',
            'Google-Sa-Jmeter-Global',
            'Google-Sa-Readme-Global',
            'Google-Sa-Hoppscotch-Global',
            'Google-Sa-Doc-Global'
          )
    """

    print("=== FINAL ACCOUNT-WIDE BIDDING HIERARCHY AUDIT ===")
    total_enabled_ags = 0
    inherited_count = 0
    override_count = 0

    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            total_enabled_ags += 1
            cname = row.campaign.name
            ag_name = row.ad_group.name
            eff_tcpa = row.ad_group.effective_target_cpa_micros / 1000000.0 if row.ad_group.effective_target_cpa_micros > 0 else 0.0
            source = row.ad_group.effective_target_cpa_source.name
            
            if row.ad_group.target_cpa_micros > 0:
                override_count += 1
                print(f"[OVERRIDE ALERT] {cname} -> {ag_name}: ${row.ad_group.target_cpa_micros/1e6:.2f}")
            else:
                inherited_count += 1

    print(f"\nAudit Summary across all 17 Campaigns:")
    print(f"  ├─ Total Active Ad Groups: {total_enabled_ags}")
    print(f"  ├─ Cleanly Inheriting from Campaign Target CPA: {inherited_count} ({(inherited_count/total_enabled_ags)*100:.1f}%)")
    print(f"  └─ Remaining Ad Group Overrides: {override_count}")

if __name__ == '__main__':
    main()
