import os
from google.ads.googleads.client import GoogleAdsClient

# Setup proxy
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# Original targeting configuration
CAMPAIGN_LOCATIONS = {
    "Google-Sa-CP-Global": [
        "geoTargetConstants/2016", # American Samoa
        "geoTargetConstants/2156", # China
        "geoTargetConstants/2316", # Guam
        "geoTargetConstants/2344", # Hong Kong
        "geoTargetConstants/2580", # Northern Mariana Islands
        "geoTargetConstants/2581", # United States Minor Outlying Islands
        "geoTargetConstants/2630", # Puerto Rico
        "geoTargetConstants/2643", # Russia
        "geoTargetConstants/2840", # United States
        "geoTargetConstants/2850"  # U.S. Virgin Islands
    ],
    "Google-Sa-Postman-Global": [
        "geoTargetConstants/2016", # American Samoa
        "geoTargetConstants/2156", # China
        "geoTargetConstants/2316", # Guam
        "geoTargetConstants/2580", # Northern Mariana Islands
        "geoTargetConstants/2581", # United States Minor Outlying Islands
        "geoTargetConstants/2630", # Puerto Rico
        "geoTargetConstants/2643", # Russia
        "geoTargetConstants/2840", # United States
        "geoTargetConstants/2850"  # U.S. Virgin Islands
    ]
}

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
          AND campaign.name IN ({','.join([f"'{c}'" for c in CAMPAIGN_LOCATIONS.keys()])})
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaigns)
    for batch in stream:
        for row in batch.results:
            campaign_ids[row.campaign.name] = str(row.campaign.id)
            
    if not campaign_ids:
        print("ERROR: Targeted campaigns not found.")
        return

    # 2. Formulate create operations for the original locations
    operations = []
    for c_name, c_id in campaign_ids.items():
        original_locs = CAMPAIGN_LOCATIONS.get(c_name, [])
        for loc in original_locs:
            print(f"Preparing to add targeting for {loc} to Campaign '{c_name}' (ID: {c_id})")
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = client.get_service("CampaignService").campaign_path(CUSTOMER_ID, c_id)
            criterion.location.geo_target_constant = loc
            operations.append(op)

    # 3. Execute CREATE operations
    if operations:
        try:
            print(f"\nExecuting {len(operations)} location restore operations...")
            response = campaign_criterion_service.mutate_campaign_criteria(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"SUCCESS: Restored {len(response.results)} campaign location criteria.")
        except Exception as e:
            print(f"ERROR restoring campaign location criteria: {e}")
    else:
        print("\nNo location criteria to restore.")
        
    print("\nDONE.")

if __name__ == "__main__":
    main()
