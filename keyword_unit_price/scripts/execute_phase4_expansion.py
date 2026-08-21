import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

expansion_data = {
    'Google-Sa-Postman-Global': {
        'Postman-Performance-Pain-Global': ['postman cloud sync alternatives', 'postman offline mode workaround', 'postman sync issues', 'postman alternative without login', 'postman too slow'],
        'Postman Alternative-Global': ['postman mock server setup', 'postman automation script', 'migrate collections from postman', 'postman collection runner alternative', 'postman ci cd integration', 'replace postman for team collaboration']
    },
    'Google-Sa-SpecFirst-Global': {
        'Stoplight-Alternative': ['swagger ui generator tools', 'swagger codegen alternative', 'auto generate swagger yaml', 'swagger editor alternative free', 'stoplight studio alternatives open source', 'openapi visual editor like stoplight', 'swagger to postman converter', 'better ui for swagger docs', 'stoplight spectral alternative', 'swagger documentation best practices']
    },
    'Google-Sa-Insomnia-Global': {
        'Insomnia api-Global': ['insomnia environment variables proxy', 'soapui rest testing framework', 'insomnia sync collections team', 'soapui pro alternative free', 'insomnia plugin for testing', 'soapui automated testing tutorial', 'insomnia graphql client', 'replace soapui for api testing', 'insomnia offline alternative desktop']
    },
    'Google-Sa-Testing-Global': {
        'Automated api testing-Global': ['ci cd api testing', 'api testing pipeline', 'api regression testing', 'automate rest api tests', 'data driven api testing', 'continuous api testing', 'api testing framework']
    },
    'Google-Sa-Doc-Global': {
        'api-document-Global': ['auto generate api docs', 'code to api docs', 'share api specs', 'java api documentation tool', 'interactive api docs', 'openapi to html', 'api doc site generator']
    },
    'Google-Sa-Mock-Global': {
        'Mock-Global': ['mock api offline', 'react mock api', 'fake api endpoint', 'dynamic mock data', 'local mock server', 'json mock server', 'simulate api errors']
    },
    'Google-Sa-Func-MultiProtocol-Global': {
        'GraphQL-gRPC': ['graphql api testing tool', 'grpc mock server', 'grpc api debugger', 'graphql query builder online', 'graphql mutation testing', 'grpc client for mac'],
        'WebSocket-SSE': ['websocket api client', 'how to test websocket connections', 'test sse endpoint online', 'websocket load testing tool']
    },
    'Google-Sa-Solutions-API-First-Global': {
        'JSON Schema Tooling': ['json schema visual editor', 'xml to json api converter', 'protobuf testing client', 'generate json schema from payload', 'validate api response against json schema', 'openapi 3.0 visual editor', 'json to typescript interface api']
    },
    'Google-Sa-Func-CICD-Global': {
        'API-Pipeline': ['github actions api testing', 'jenkins api test automation', 'gitlab ci api mock server', 'bitbucket pipelines api test', 'azure devops api testing task', 'circleci api automation', 'integrate api tests into ci cd', 'run api tests on git push']
    },
    'Google-Sa-Comp-VSCode-Global': {
        'Thunder-Client': ['thunder client alternatives', 'postman vs thunder client vscode'],
        'REST-Client': ['vscode api client plugin', 'intellij api tester extension', 'rest client vscode alternative', 'test apis directly in vscode', 'webstorm api client', 'vscode extension for api mocking']
    }
}

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    
    operations = []
    
    for camp_name, adgroups in expansion_data.items():
        for adgroup_name, keywords in adgroups.items():
            # 1. Lookup Ad Group Resource Name by Campaign Name and Ad Group Name
            query = f"""
                SELECT ad_group.resource_name, ad_group.id
                FROM ad_group 
                WHERE campaign.name = '{camp_name}' 
                  AND ad_group.name = '{adgroup_name}' 
                  AND ad_group.status = 'ENABLED' 
                LIMIT 1
            """
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            ad_group_resource_name = None
            
            for batch in stream:
                for row in batch.results:
                    ad_group_resource_name = row.ad_group.resource_name
                    break
                if ad_group_resource_name:
                    break
                    
            if not ad_group_resource_name:
                print(f"[Warning] Could not find enabled Ad Group '{adgroup_name}' in Campaign '{camp_name}'. Skipping.")
                continue
                
            print(f"Found Ad Group: {adgroup_name} ({ad_group_resource_name})")
            
            # 2. Build operations for this Ad Group
            for kw in keywords:
                operation = client.get_type("AdGroupCriterionOperation")
                criterion = operation.create
                criterion.ad_group = ad_group_resource_name
                criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                criterion.keyword.text = kw
                criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE # Strict control
                
                operations.append(operation)

    if operations:
        print(f"\nReady to upload {len(operations)} new EXACT/PHRASE match keywords...")
        try:
            request = client.get_type("MutateAdGroupCriteriaRequest")
            request.customer_id = CUSTOMER_ID
            request.operations = operations
            request.partial_failure = True
            response = ad_group_criterion_service.mutate_ad_group_criteria(request=request)
            print(f"Successfully added expansion keywords to Google Ads.")
        except GoogleAdsException as ex:
            print(f"Request failed with status '{ex.error.code().name}':")
            for error in ex.failure.errors:
                print(f"\tError: {error.message}")
    else:
        print("No operations to execute.")

if __name__ == "__main__":
    main()
