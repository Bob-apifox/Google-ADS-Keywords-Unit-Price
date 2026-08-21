import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

TARGET_CAMPAIGNS = ['Google-Sa-Testing-Global', 'Google-Sa-Mock-Global', 'Google-Sa-Readme-Global']
MIN_CONVERSIONS = 10
TARGET_CPA_LIMIT = 5.0 # Max CPA to consider it 'healthy'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
    # Format list for GAQL
    camp_names_str = ", ".join([f"'{c}'" for c in TARGET_CAMPAIGNS])
    
    # Query performance over the last 30 days
    query = f"""
        SELECT 
            ad_group_criterion.resource_name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            metrics.conversions,
            metrics.cost_micros,
            campaign.name
        FROM keyword_view 
        WHERE campaign.name IN ({camp_names_str})
          AND ad_group_criterion.status = 'ENABLED'
          AND campaign.status = 'ENABLED'
          AND segments.date DURING LAST_30_DAYS
          AND metrics.conversions > {MIN_CONVERSIONS}
    """
    
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        operations = []
        
        for batch in stream:
            for row in batch.results:
                kw = row.ad_group_criterion
                metrics = row.metrics
                
                # Check match type (only upgrade EXACT or PHRASE)
                if kw.keyword.match_type.name == 'BROAD':
                    continue
                    
                conversions = metrics.conversions
                cost = metrics.cost_micros / 1000000
                cpa = cost / conversions if conversions > 0 else 0
                
                if cpa <= TARGET_CPA_LIMIT:
                    print(f"Upgrading '{kw.keyword.text}' in '{row.campaign.name}' (Conv: {conversions}, CPA: ${cpa:.2f}) to BROAD")
                    
                    operation = client.get_type("AdGroupCriterionOperation")
                    criterion = operation.update
                    criterion.resource_name = kw.resource_name
                    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
                    
                    # Update mask
                    from google.api_core import protobuf_helpers
                    client.copy_from(operation.update_mask, protobuf_helpers.field_mask(None, criterion._pb))
                    operations.append(operation)

        if operations:
            response = ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"✅ Successfully upgraded {len(response.results)} keywords to BROAD match.")
        else:
            print("No keywords met the criteria for Broad Match upgrade.")
            
    except GoogleAdsException as ex:
        print(f"Request failed with status '{ex.error.code().name}':")
        for error in ex.failure.errors:
            print(f"\tError: {error.message}")

if __name__ == "__main__":
    main()
