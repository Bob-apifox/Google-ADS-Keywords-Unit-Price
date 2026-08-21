import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

SECTION_5_TARGETS = {
    "Google-Sa-CP-Global": {"target_budget": 180.0, "target_tcpa": 2.30},
    "Google-Sa-Postman-Global": {"target_budget": 95.0, "target_tcpa": 2.90},
    "Google-Sa-DSA-Alternatives-Global": {"target_budget": 50.0, "target_tcpa": 2.50},
    "Google-Sa-Comp-HeavyQA-Global": {"target_budget": 45.0, "target_tcpa": 2.50},
    "Google-Sa-Func-MultiProtocol-Global": {"target_budget": 30.0, "target_tcpa": 2.50},
    "Google-Sa-Category-Competitor-Global": {"target_budget": 35.0, "target_tcpa": 2.50},
    "Google-Sa-CP-TW": {"target_budget": 15.0, "target_tcpa": 2.50},
    "Google-PMax-CP-Global": {"target_budget": 50.0, "target_tcpa": 3.50},
    "Google-PMax-Postman": {"target_budget": 30.0, "target_tcpa": 4.00},
    "Google-Sa-Solutions-AI-LLM-Global": {"target_budget": 120.0, "target_tcpa": 2.50},
    "Google-Sa-Stoplight-Global": {"target_budget": 12.0, "target_tcpa": 3.00},
    "Google-Sa-Insomnia-Global": {"target_budget": 12.0, "target_tcpa": 3.00},
    "Google-Sa-MCP-Infrastructure": {"target_budget": 10.0, "target_tcpa": 2.50},
    "Google-Sa-Jmeter-Global": {"target_budget": 65.0, "target_tcpa": 3.50},
    "Google-Sa-Readme-Global": {"target_budget": 55.0, "target_tcpa": 3.00},
    "Google-Sa-Hoppscotch-Global": {"target_budget": 30.0, "target_tcpa": 2.50},
    "Google-Sa-Doc-Global": {"target_budget": 25.0, "target_tcpa": 2.50}
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    names_str = ", ".join([f"'{n}'" for n in SECTION_5_TARGETS.keys()])
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN ({names_str})
    """
    
    print("=================================================================================================================")
    print(f"{'Campaign Name':<36} | {'Live Budget':<12} | {'Plan Budget':<12} | {'Live tCPA':<11} | {'Plan tCPA':<11} | {'Status'}")
    print("=================================================================================================================")
    
    pending_adjustments = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            c = row.campaign
            cname = c.name
            b_live = row.campaign_budget.amount_micros / 1000000.0
            tcpa_live = (c.maximize_conversions.target_cpa_micros or c.target_cpa.target_cpa_micros) / 1000000.0
            
            target = SECTION_5_TARGETS.get(cname, {})
            b_target = target.get("target_budget", b_live)
            tcpa_target = target.get("target_tcpa", tcpa_live)
            
            b_diff = abs(b_live - b_target) > 0.01
            tcpa_diff = abs(tcpa_live - tcpa_target) > 0.01
            
            status_str = "ALIGNED (OK)"
            if b_diff or tcpa_diff:
                status_str = "NEEDS ADJUSTMENT"
                pending_adjustments[cname] = {
                    'live_b': b_live, 'target_b': b_target,
                    'live_tcpa': tcpa_live, 'target_tcpa': tcpa_target
                }
                
            print(f"{cname:<36} | ${b_live:<11.2f} | ${b_target:<11.2f} | ${tcpa_live:<10.2f} | ${tcpa_target:<10.2f} | {status_str}")

    print("\n=================================================================================================================")
    print(f"Total Campaigns Checked: {len(SECTION_5_TARGETS)} | Pending Adjustments: {len(pending_adjustments)}")
    print("=================================================================================================================")
    for k, v in pending_adjustments.items():
        print(f"  👉 [{k}]")
        if abs(v['live_b'] - v['target_b']) > 0.01:
            print(f"     Budget: ${v['live_b']:.2f} -> ${v['target_b']:.2f}/day")
        if abs(v['live_tcpa'] - v['target_tcpa']) > 0.01:
            print(f"     Target CPA: ${v['live_tcpa']:.2f} -> ${v['target_tcpa']:.2f}")

if __name__ == '__main__':
    main()
