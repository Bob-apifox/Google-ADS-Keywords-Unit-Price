import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

expansion_plan = {
    # Campaign ID: (Keyword text, Match Type)
    23440301503: ("top 10 API tools", "PHRASE"),
    22146873045: ("online api tool", "PHRASE")
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
    operations = []
    
    for camp_id, (kw_text, match_type) in expansion_plan.items():
        # Query for the first active Ad Group in the Campaign
        query = f'''
            SELECT ad_group.resource_name, ad_group.name 
            FROM ad_group 
            WHERE campaign.id = {camp_id} AND ad_group.status = 'ENABLED' 
            LIMIT 1
        '''
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        ad_group_resource_name = None
        for batch in stream:
            for row in batch.results:
                ad_group_resource_name = row.ad_group.resource_name
                break
            if ad_group_resource_name:
                break
                
        if ad_group_resource_name:
            print(f"Adding '{kw_text}' to Ad Group: {ad_group_resource_name}")
            
            operation = client.get_type("AdGroupCriterionOperation")
            criterion = operation.create
            criterion.ad_group = ad_group_resource_name
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw_text
            
            if match_type == "EXACT":
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            elif match_type == "PHRASE":
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                
            operations.append(operation)
        else:
            print(f"No active Ad Group found for Campaign ID {camp_id}")

    if operations:
        try:
            response = ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"Added {len(response.results)} new expansion keywords.")
        except GoogleAdsException as ex:
            print(f"Request failed with status '{ex.error.code().name}':")
            for error in ex.failure.errors:
                print(f"\tError: {error.message}")

if __name__ == "__main__":
    main()
