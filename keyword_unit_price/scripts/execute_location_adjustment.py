import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

TARGET_CAMPAIGNS = ["Google-Sa-CP-Global", "Google-Sa-Postman-Global"]
TARGET_COUNTRIES = {
    "Brazil": "geoTargetConstants/2076",      # Geo target ID for Brazil is 2076
    "Indonesia": "geoTargetConstants/2360"    # Geo target ID for Indonesia is 2360
}
BID_MODIFIER = 1.10  # +10% bid adjustment

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
            campaign_ids[row.campaign.name] = row.campaign.id
            
    if not campaign_ids:
        print("ERROR: Targeted campaigns not found.")
        return

    # 2. Check existing location criteria for these campaigns
    print("\n>>> Checking existing location criteria...")
    existing_locations = {}  # (campaign_id, geo_target_constant_resource) -> (criterion_id, current_modifier)
    
    # Locations query
    query_locations = """
        SELECT 
            campaign.id,
            campaign_criterion.criterion_id,
            campaign_criterion.location.geo_target_constant,
            campaign_criterion.bid_modifier
        FROM campaign_criterion
        WHERE campaign_criterion.type = 'LOCATION'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_locations)
    for batch in stream:
        for row in batch.results:
            c_id = str(row.campaign.id)
            if c_id in campaign_ids.values():
                criterion_id = row.campaign_criterion.criterion_id
                geo_constant = row.campaign_criterion.location.geo_target_constant
                bid_modifier = row.campaign_criterion.bid_modifier
                existing_locations[(c_id, geo_constant)] = (criterion_id, bid_modifier)

    # 3. Formulate operations (create or update)
    print("\n>>> Preparing operations...")
    operations = []
    
    for c_name, c_id in campaign_ids.items():
        c_id_str = str(c_id)
        for country_name, geo_resource_path in TARGET_COUNTRIES.items():
            geo_resource = f"geoTargetConstants/{geo_resource_path.split('/')[-1]}"
            key = (c_id_str, geo_resource)
            
            if key in existing_locations:
                criterion_id, current_modifier = existing_locations[key]
                print(f"Campaign '{c_name}': Location '{country_name}' already exists (ID: {criterion_id}). Current modifier: {current_modifier}")
                
                # Check if modifier needs updating
                if current_modifier != BID_MODIFIER:
                    op = client.get_type("CampaignCriterionOperation")
                    criterion = op.update
                    criterion.resource_name = campaign_criterion_service.campaign_criterion_path(CUSTOMER_ID, c_id_str, criterion_id)
                    criterion.bid_modifier = BID_MODIFIER
                    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, criterion._pb))
                    operations.append(op)
                    print(f"  -> Added UPDATE operation to change modifier to {BID_MODIFIER}")
            else:
                print(f"Campaign '{c_name}': Location '{country_name}' not found. Creating new target with modifier {BID_MODIFIER}")
                op = client.get_type("CampaignCriterionOperation")
                criterion = op.create
                criterion.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id_str)
                criterion.location.geo_target_constant = geo_resource
                criterion.bid_modifier = BID_MODIFIER
                operations.append(op)
                print(f"  -> Added CREATE operation")

    # 4. Mutate criteria
    if operations:
        try:
            print(f"\nExecuting {len(operations)} location operations...")
            response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=operations)
            print(f"SUCCESS: Mutated {len(response.results)} campaign location criteria.")
        except Exception as e:
            print(f"ERROR mutating campaign location criteria: {e}")
    else:
        print("\nNo location adjustments needed. Everything is up to date!")
        
    print("\nDONE.")

if __name__ == "__main__":
    main()
