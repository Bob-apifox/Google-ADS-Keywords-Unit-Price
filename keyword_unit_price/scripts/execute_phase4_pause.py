import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")
    
    query = """
        SELECT ad_group.resource_name, ad_group.name, campaign.name 
        FROM ad_group 
        WHERE ad_group.name = 'Ad group 1' 
          AND ad_group.status = 'ENABLED'
          AND campaign.status = 'ENABLED'
    """
    
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        operations = []
        for batch in stream:
            for row in batch.results:
                print(f"Pausing '{row.ad_group.name}' in Campaign '{row.campaign.name}'")
                operation = client.get_type("AdGroupOperation")
                ad_group = operation.update
                ad_group.resource_name = row.ad_group.resource_name
                ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
                client.copy_from(operation.update_mask, client.field_mask(None, ad_group))
                operations.append(operation)
                
        if operations:
            response = ad_group_service.mutate_ad_groups(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"✅ Successfully paused {len(response.results)} ad groups.")
        else:
            print("No active 'Ad group 1' found to pause.")
            
    except GoogleAdsException as ex:
        print(f"Request failed with status '{ex.error.code().name}':")
        for error in ex.failure.errors:
            print(f"\tError: {error.message}")

if __name__ == "__main__":
    main()
