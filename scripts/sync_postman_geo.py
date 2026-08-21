import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_criterion_service = client.get_service('CampaignCriterionService')
campaign_service = client.get_service('CampaignService')
customer_id = '9496728294'

search_campaign_id = '21982653330' # Google-Sa-Postman-Global
pmax_campaign_id = '23685533966' # Google-PMax-Postman

def sync_negative_geos():
    print(">>> Fetching negative geos from Google-Sa-Postman-Global...")
    query_search = f"""
        SELECT campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign.id = {search_campaign_id}
        AND campaign_criterion.negative = TRUE
        AND campaign_criterion.type = 'LOCATION'
    """
    
    search_geos = set()
    stream = ga_service.search_stream(customer_id=customer_id, query=query_search)
    for batch in stream:
        for row in batch.results:
            search_geos.add(row.campaign_criterion.location.geo_target_constant)
            
    print(f"Found {len(search_geos)} negative locations in Search campaign.")
    
    # Get existing negative geos in PMax
    query_pmax = f"""
        SELECT campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign.id = {pmax_campaign_id}
        AND campaign_criterion.negative = TRUE
        AND campaign_criterion.type = 'LOCATION'
    """
    
    pmax_geos = set()
    stream_pmax = ga_service.search_stream(customer_id=customer_id, query=query_pmax)
    for batch in stream_pmax:
        for row in batch.results:
            pmax_geos.add(row.campaign_criterion.location.geo_target_constant)
            
    geos_to_add = search_geos - pmax_geos
    print(f"Found {len(geos_to_add)} new negative locations to add to PMax.")
    
    if not geos_to_add:
        print("PMax campaign is already synced. Nothing to do.")
        return
        
    ops = []
    for geo in geos_to_add:
        op = client.get_type('CampaignCriterionOperation')
        criterion = op.create
        criterion.campaign = campaign_service.campaign_path(customer_id, pmax_campaign_id)
        criterion.type_ = client.enums.CriterionTypeEnum.LOCATION
        # geo_target_constant string is already full path e.g. "geoTargetConstants/2840"
        criterion.location.geo_target_constant = geo
        criterion.negative = True
        ops.append(op)
        
    try:
        resp = campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=ops)
        print(f"Successfully added {len(resp.results)} negative locations to Google-PMax-Postman.")
    except Exception as e:
        print(f"Error adding negative locations: {e}")

if __name__ == '__main__':
    sync_negative_geos()
