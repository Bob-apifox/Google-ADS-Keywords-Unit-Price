import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
CAMPAIGN_NAME = 'Google-Sa-CLI-Terminal-Global'

def execute():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service('GoogleAdsService')
        
        # 1. Fetch Campaign
        q_camp = f"SELECT campaign.id, campaign.resource_name FROM campaign WHERE campaign.name = '{CAMPAIGN_NAME}'"
        camp_res = None
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
            for row in batch.results:
                camp_res = row.campaign.resource_name
                print(f"Found campaign: {CAMPAIGN_NAME} (Resource: {camp_res})")
                break
                
        if not camp_res:
            print(f"Could not find campaign: {CAMPAIGN_NAME}")
            return

        # 2. Known Standard Geo IDs for US and Territories
        # 2840 - United States
        # 2016 - American Samoa
        # 2316 - Guam
        # 2580 - Northern Mariana Islands
        # 2630 - Puerto Rico
        # 2581 - United States Minor Outlying Islands
        # 2850 - U.S. Virgin Islands
        final_geo_ids = [2840, 2016, 2316, 2580, 2630, 2581, 2850]

        # 3. Apply Negative Campaign Criteria
        camp_crit_service = client.get_service('CampaignCriterionService')
        geo_target_constant_service = client.get_service('GeoTargetConstantService')
        
        ops = []
        for gid in final_geo_ids:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = camp_res
            crit.negative = True
            crit.location.geo_target_constant = geo_target_constant_service.geo_target_constant_path(str(gid))
            ops.append(op)
            
        print(f"Applying {len(ops)} Negative Location Exclusions...")
        
        # Partial failure is helpful to ignore duplicates if already excluded
        req = client.get_type("MutateCampaignCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        req.partial_failure = True
        
        resp = camp_crit_service.mutate_campaign_criteria(request=req)
        
        if resp.partial_failure_error and resp.partial_failure_error.details:
            print("Some locations might already be excluded or invalid (Partial Failure Details):")
            for err in resp.partial_failure_error.details:
                print(f"Error: {err}")
        else:
            print(f"Successfully excluded locations.")

    except GoogleAdsException as ex:
        print(f"GoogleAdsException occurred: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")

if __name__ == '__main__':
    execute()
