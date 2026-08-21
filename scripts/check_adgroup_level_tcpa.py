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
    "Google-Sa-MCP-Infrastructure",
    "Google-Sa-Func-CICD-Global",
    "Google-PMax-Postman",
    "Google-Sa-Jmeter-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Solutions-AI-LLM-Global",
    "Google-Sa-Postman-Global",
    "Google-Sa-CP-Global",
    "Google-Sa-Comp-HeavyQA-Global",
    "Google-Sa-Func-MultiProtocol-Global",
    "Google-Sa-DSA-Alternatives-Global"
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
    
    print("=== CHECKING AD GROUP LEVEL TARGET CPA vs CAMPAIGN LEVEL ===")
    results = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            cname = row.campaign.name
            cid = row.campaign.id
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            ag_status = row.ad_group.status.name
            ag_tcpa_explicit = row.ad_group.target_cpa_micros / 1000000.0 if row.ad_group.target_cpa_micros > 0 else None
            eff_tcpa = row.ad_group.effective_target_cpa_micros / 1000000.0 if row.ad_group.effective_target_cpa_micros > 0 else 0.0
            source = row.ad_group.effective_target_cpa_source.name
            
            c_tcpa = (row.campaign.maximize_conversions.target_cpa_micros or row.campaign.target_cpa.target_cpa_micros) / 1000000.0
            
            if cname not in results:
                results[cname] = {'cid': cid, 'c_tcpa': c_tcpa, 'ad_groups': []}
            results[cname]['ad_groups'].append({
                'id': ag_id, 'name': ag_name, 'status': ag_status,
                'explicit_tcpa': ag_tcpa_explicit, 'effective_tcpa': eff_tcpa, 'source': source
            })

    for cname, data in results.items():
        print(f"\n[Campaign] {cname} (ID: {data['cid']}) | Campaign-Level tCPA: ${data['c_tcpa']:.2f}")
        for ag in data['ad_groups']:
            override_str = f"** EXPLICIT OVERRIDE: ${ag['explicit_tcpa']:.2f} **" if ag['explicit_tcpa'] else "Inherited from Campaign"
            print(f"   └─ Ad Group: {ag['name']:<32} (ID: {ag['id']}) | Status: {ag['status']:<7} | Effective tCPA: ${ag['effective_tcpa']:.2f} ({ag['source']}) | {override_str}")

if __name__ == '__main__':
    main()
