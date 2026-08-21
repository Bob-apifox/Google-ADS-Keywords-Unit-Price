import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'
CAMPAIGN_ID = 23974416637

def create_ad_group(client, customer_id, campaign_id):
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = "Terminal-Native-Clients"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = 1000000

    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = ad_group_response.results[0].resource_name
    print(f"Created ad group: {ad_group_resource_name}")
    return ad_group_resource_name

def add_keywords(client, customer_id, ad_group_resource_name):
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    keywords = [
        "terminal based api client",
        "cli http client",
        "command line rest client",
        "test api from terminal",
        "terminal api tester"
    ]
    operations = []
    for kw in keywords:
        operation = client.get_type("AdGroupCriterionOperation")
        criterion = operation.create
        criterion.ad_group = ad_group_resource_name
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        operations.append(operation)
        
    response = ag_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )
    print(f"Added {len(response.results)} keywords.")

def create_rsa(client, customer_id, ad_group_resource_name):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad_group_ad.ad.final_urls.append("https://apidog.com/features/cli")
    ad_group_ad.ad.tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
    
    # Headlines
    headlines = [
        "Ultimate Terminal API Client",
        "Faster API Testing in CLI",
        "Keyboard-First API Tester",
        "Test REST & GraphQL in CLI",
        "Better Than cURL for APIs",
        "The CLI Tool for API Devs",
        "Test APIs Without a Mouse",
        "Advanced Terminal API Client",
        "Stop Typing Long cURL Commands",
        "Send HTTP Requests in CLI",
        "Build & Test APIs in Terminal",
        "Lightweight API Client for CLI",
        "Integrate CLI with CI/CD",
        "Beautiful UI in Your Terminal",
        "Seamless API Testing in CLI"
    ]
    for h in headlines:
        ad_text_asset = client.get_type("AdTextAsset")
        ad_text_asset.text = h
        ad_group_ad.ad.responsive_search_ad.headlines.append(ad_text_asset)
        
    # Descriptions
    descriptions = [
        "Ditch cURL. Test REST, GraphQL & WebSockets directly from your terminal.",
        "Integrates with your CI/CD. No mouse required. Built for developers.",
        "The ultimate command-line API client for testing, debugging, and automation.",
        "Save time testing APIs. A keyboard-first HTTP client designed for modern devs."
    ]
    for d in descriptions:
        ad_text_asset = client.get_type("AdTextAsset")
        ad_text_asset.text = d
        ad_group_ad.ad.responsive_search_ad.descriptions.append(ad_text_asset)
        
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    print(f"Created responsive search ad: {response.results[0].resource_name}")

def main():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        
        # Ad group and keywords were already created successfully.
        ad_group_resource_name = "customers/9496728294/adGroups/198424491739"
        
        print("Creating Ad...")
        create_rsa(client, CUSTOMER_ID, ad_group_resource_name)
        print("Successfully built the new Terminal-Native-Clients ad group.")
    except GoogleAdsException as ex:
        print(f"Request with ID '{ex.request_id}' failed with status "
              f"'{ex.error.code().name}' and includes the following errors:")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)

if __name__ == "__main__":
    main()
