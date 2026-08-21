import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

negative_plan = {
    'Google-Sa-CLI-Global': ['postman online', 'online postman'],
    'Google-Sa-SpecFirst-Global': ['free api testing tools', 'zapier ai', 'backendless'],
    'Google-Sa-Bruno-Global': ['openrouter api', 'workflow', 'https ngrok com'],
    'Google-Sa-Stoplight-Global': ['code visualstudio com', 'online rest api', 'ocr api'],
    'Google-Sa-Mock-Global': ['browserstack', 'appetize io', 'glide apps', 'v0 by vercel'],
    'Google-Sa-Doc-Global': ['dogapi', 'nanonets', 'ai documentation generator'],
    'Google-Sa-Mintlify-Global': ['next js', 'rest client online', 'notion', 'redoc'],
    'Google-Sa-Func-MultiProtocol-Global': ['graphql playground download', 'websocket tester']
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    
    operations = []
    
    for camp_name, negatives in negative_plan.items():
        # Lookup Campaign Resource Name
        query = f"SELECT campaign.resource_name FROM campaign WHERE campaign.name = '{camp_name}' AND campaign.status = 'ENABLED' LIMIT 1"
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        camp_resource = None
        for batch in stream:
            for row in batch.results:
                camp_resource = row.campaign.resource_name
                break
            if camp_resource:
                break
                
        if camp_resource:
            print(f"Found Campaign: {camp_name} ({camp_resource})")
            for neg in negatives:
                operation = client.get_type("CampaignCriterionOperation")
                criterion = operation.create
                criterion.campaign = camp_resource
                criterion.negative = True
                criterion.keyword.text = neg
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT # Usually EXACT for search terms
                operations.append(operation)
        else:
            print(f"[Warning] Could not find enabled Campaign '{camp_name}'.")

    if operations:
        try:
            response = campaign_criterion_service.mutate_campaign_criteria(
                customer_id=CUSTOMER_ID, operations=operations
            )
            print(f"Successfully added {len(response.results)} negative keywords.")
        except GoogleAdsException as ex:
            print(f"Request failed with status '{ex.error.code().name}':")
            for error in ex.failure.errors:
                print(f"\tError: {error.message}")
    else:
        print("No operations to execute.")

if __name__ == "__main__":
    main()
