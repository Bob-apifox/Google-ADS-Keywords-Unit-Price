import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')

    # Query AdGroupCriterion for Webpage criteria
    query = """
        SELECT 
            campaign.name,
            ad_group.name,
            ad_group_criterion.webpage.conditions,
            ad_group_criterion.webpage.criterion_name,
            ad_group_criterion.status
        FROM ad_group_criterion 
        WHERE ad_group_criterion.type = 'WEBPAGE'
          AND ad_group_criterion.status != 'REMOVED'
    """
    
    found = False
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=query):
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            conditions = []
            for cond in row.ad_group_criterion.webpage.conditions:
                conditions.append(cond.argument)
            
            cond_str = ", ".join(conditions)
            print(f"Campaign: {c_name} | AdGroup: {ag_name} | Targets: {cond_str}")
            if "soapui" in cond_str.lower():
                found = True

    if not found:
        print("Did not find any explicit SOAPUI targets in DSA.")

if __name__ == '__main__':
    execute()
