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
    
    # 1. Search for campaigns with TW, SG, AU, KR in their name or Geo Targets
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign_budget.amount_micros,
            campaign.bidding_strategy_type
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    
    print("=== All Active Campaigns ===")
    active_campaigns = []
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            budget_usd = row.campaign_budget.amount_micros / 1000000.0
            active_campaigns.append({
                'id': str(row.campaign.id),
                'name': row.campaign.name,
                'budget': budget_usd,
                'bidding': row.campaign.bidding_strategy_type.name
            })
            print(f"ID: {row.campaign.id} | Name: {row.campaign.name} | Budget: ${budget_usd:.2f} | Bidding: {row.campaign.bidding_strategy_type.name}")

    # 2. Check Ad Groups for specific campaigns like Google-Sa-CP-TW, Google-Sa-CP-KR, or Postman/Global
    target_camps = [c for c in active_campaigns if any(k in c['name'] for k in ['TW', 'KR', 'SG', 'AU', 'Postman', 'CP-Global'])]
    print("\n=== Ad Groups for Target Campaigns ===")
    for tc in target_camps:
        cid = tc['id']
        ag_query = f"""
            SELECT
                ad_group.id,
                ad_group.name,
                ad_group.status
            FROM ad_group
            WHERE campaign.id = {cid} AND ad_group.status = 'ENABLED'
        """
        print(f"\nCampaign: {tc['name']} ({cid})")
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=ag_query):
            for row in batch.results:
                print(f"  └─ Ad Group: {row.ad_group.name} (ID: {row.ad_group.id})")

if __name__ == '__main__':
    main()
