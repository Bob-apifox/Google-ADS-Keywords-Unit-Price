import os
from google.ads.googleads.client import GoogleAdsClient

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGET_CAMPAIGNS = ["Google-Sa-CP-Global", "Google-Sa-Postman-Global"]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    
    # 1. Fetch Campaign IDs
    campaign_ids = {}
    print(">>> Fetching campaign details...")
    query_campaigns = f"""
        SELECT campaign.id, campaign.name 
        FROM campaign 
        WHERE campaign.status = 'ENABLED' 
          AND campaign.name IN ({','.join([f"'{c}'" for c in TARGET_CAMPAIGNS])})
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaigns)
    for batch in stream:
        for row in batch.results:
            campaign_ids[row.campaign.name] = str(row.campaign.id)
            
    if not campaign_ids:
        print("ERROR: Targeted campaigns not found.")
        return

    print(f"Found campaigns: {campaign_ids}")

    # 2. Query location criteria for these campaigns
    print("\n>>> Checking existing location criteria...")
    query_locations = """
        SELECT 
            campaign.id,
            campaign.name,
            campaign_criterion.criterion_id,
            campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'LOCATION'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_locations)
    
    operations = []
    for batch in stream:
        for row in batch.results:
            c_id = str(row.campaign.id)
            if c_id in campaign_ids.values():
                criterion_id = row.campaign_criterion.criterion_id
                geo_constant = row.campaign_criterion.location.geo_target_constant
                c_name = row.campaign.name
                
                resource_name = campaign_criterion_service.campaign_criterion_path(
                    CUSTOMER_ID, c_id, criterion_id
                )
                print(f"Found location criterion on Campaign '{c_name}': {geo_constant} (ID: {criterion_id}) -> Resource: {resource_name}")
                
                # Create REMOVE operation
                op = client.get_type("CampaignCriterionOperation")
                op.remove = resource_name
                operations.append(op)

    # 3. Execute REMOVE operations
    if operations:
        try:
            print(f"\nExecuting {len(operations)} location removal operations...")
            response = campaign_criterion_service.mutate_campaign_criteria(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"SUCCESS: Removed {len(response.results)} campaign location criteria.")
            print("Targeting should now revert back to global (All countries and territories).")
        except Exception as e:
            print(f"ERROR removing campaign location criteria: {e}")
    else:
        print("\nNo location criteria found to remove.")
        
    print("\nDONE.")

if __name__ == "__main__":
    main()
