import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGET_CAMPAIGNS = [
    "Google-Sa-Stoplight-Global",
    "Google-Sa-Insomnia-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Postman-Global",
    "Google-Sa-CP-Global"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    
    names_str = ", ".join([f"'{n}'" for n in TARGET_CAMPAIGNS])
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros,
            ad_group.id,
            ad_group.name,
            ad_group.status,
            ad_group.target_cpa_micros,
            ad_group.effective_target_cpa_micros,
            ad_group.effective_target_cpa_source
        FROM ad_group
        WHERE campaign.name IN ({names_str})
          AND ad_group.status != 'REMOVED'
    """
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            cname = row.campaign.name
            ag_name = row.ad_group.name
            ag_status = row.ad_group.status.name
            ag_tcpa_explicit = row.ad_group.target_cpa_micros / 1000000.0 if row.ad_group.target_cpa_micros > 0 else None
            eff_tcpa = row.ad_group.effective_target_cpa_micros / 1000000.0 if row.ad_group.effective_target_cpa_micros > 0 else 0.0
            source = row.ad_group.effective_target_cpa_source.name
            
            c_tcpa = (row.campaign.maximize_conversions.target_cpa_micros or row.campaign.target_cpa.target_cpa_micros) / 1000000.0
            
            override_str = f"** OVERRIDE: ${ag_tcpa_explicit:.2f} **" if ag_tcpa_explicit else "Inherited from Campaign"
            print(f"[{cname}] | AG: {ag_name:<30} ({ag_status}) | Eff tCPA: ${eff_tcpa:.2f} ({source}) | {override_str}")

if __name__ == '__main__':
    main()
