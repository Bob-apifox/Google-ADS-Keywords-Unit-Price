import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
ad_group_service = client.get_service("AdGroupService")
ag_criterion_service = client.get_service("AdGroupCriterionService")
ad_group_ad_service = client.get_service("AdGroupAdService")
customer_id = '9496728294'

def unlock_swagger_cpc():
    q = "SELECT ad_group.id, ad_group.name, ad_group.cpc_bid_micros FROM ad_group WHERE campaign.name = 'Google-Sa-Swagger-Global' AND ad_group.status = 'ENABLED'"
    stream = ga_service.search_stream(customer_id=customer_id, query=q)
    ops = []
    for batch in stream:
        for row in batch.results:
            op = client.get_type('AdGroupOperation')
            ag = op.update
            ag.resource_name = ad_group_service.ad_group_path(customer_id, row.ad_group.id)
            ag.cpc_bid_micros = 1500000 # $1.50
            op.update_mask.paths.append("cpc_bid_micros")
            ops.append(op)
    if ops:
        ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=ops)
        print(">>> Successfully unlocked Swagger $0.01 CPC limit -> $1.50")

def get_campaign_id(camp_name):
    q = f"SELECT campaign.id FROM campaign WHERE campaign.name = '{camp_name}' LIMIT 1"
    stream = ga_service.search_stream(customer_id=customer_id, query=q)
    for batch in stream:
        for row in batch.results:
            return row.campaign.id
    return None

def create_full_ad_group(camp_name, ag_name, keywords, final_url, headlines, descriptions):
    camp_id = get_campaign_id(camp_name)
    if not camp_id:
        print(f"Error: Campaign {camp_name} not found.")
        return
        
    print(f"\n>>> Creating AdGroup: {ag_name} in {camp_name}")
    # 1. Create Ad Group
    ag_op = client.get_type("AdGroupOperation")
    ad_group = ag_op.create
    ad_group.name = ag_name
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = client.get_service("CampaignService").campaign_path(customer_id, camp_id)
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ad_group.cpc_bid_micros = 1000000
    
    ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
    ag_res = ag_resp.results[0].resource_name
    print(f"Created: {ag_res}")
    
    # 2. Add Keywords
    kw_ops = []
    for kw in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.create
        criterion.ad_group = ag_res
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = kw.replace('[', '').replace(']', '')
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT if '[' in kw else client.enums.KeywordMatchTypeEnum.BROAD
        kw_ops.append(op)
    if kw_ops:
        ag_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=kw_ops)
        print(f"Added {len(kw_ops)} keywords.")
        
    # 3. Create RSA
    ad_op = client.get_type("AdGroupAdOperation")
    ad = ad_op.create
    ad.ad_group = ag_res
    ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad.ad.final_urls.append(final_url)
    ad.ad.tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
    
    for h in headlines:
        asset = client.get_type("AdTextAsset")
        asset.text = h
        ad.ad.responsive_search_ad.headlines.append(asset)
    for d in descriptions:
        asset = client.get_type("AdTextAsset")
        asset.text = d
        ad.ad.responsive_search_ad.descriptions.append(asset)
        
    ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
    print(f"Created RSA for {ag_name}.")

if __name__ == '__main__':
    unlock_swagger_cpc()
    
    # 1. API Docs
    create_full_ad_group(
        'Google-Sa-Swagger-Global', 'API-Docs-Generation',
        ['[redoc alternative]', '[stoplight alternative]', '[readme alternative]', 'swagger ui generator', 'auto generate api docs', 'create interactive api documentation', 'api documentation software', 'generate api docs from postman', 'openapi viewer'],
        'https://apidog.com/api-doc/',
        ["Best API Documentation Tool", "Beautiful API Documentation", "Auto-Generate API Docs", "Interactive API Docs", "Stop Syncing Docs Manually", "Swagger UI Alternative", "Better Than Redoc", "OpenAPI to Docs Instantly", "Zero Code API Documentation", "Share APIs with Your Team", "Professional API Portal", "Free API Documentation Tool", "#1 API Design Platform", "Seamless API Collaboration", "Try Apidog for Free Today"],
        ["Stop syncing docs manually. Generate interactive API docs instantly from OpenAPI specs.", "Build a beautiful, customized API developer portal in minutes. Try Apidog for free.", "The ultimate alternative to Swagger UI and Redoc. Auto-generate docs from your code.", "Enhance developer experience with beautiful, interactive, and shareable documentation."]
    )
    
    # 2. Mocking
    create_full_ad_group(
        'Google-Sa-Mock-Global', 'Mock-Server-Frontend',
        ['[mockoon alternative]', '[wiremock alternative]', '[beeceptor alternative]', 'json server alternative', 'mock api server online', 'fake rest api generator', 'api mock server open source', 'simulate api response', 'mock api for frontend testing'],
        'https://apidog.com/api-mocking/',
        ["Smart API Mock Server", "Best Mockoon Alternative", "Fake REST API Generator", "Unblock Your Frontend Team", "Generate Mock Data Instantly", "Local API Mocking Tool", "Better Than JSON Server", "Open Source Mock Server", "Dynamic Mock API Data", "Zero-Code Mocking Engine", "OpenAPI to Mock Server", "Start Mocking APIs for Free", "Frontend Development Tool", "Simulate API Responses", "Try Apidog for Free Today"],
        ["Generate dynamic fake data instantly without writing backend code. 100% realistic.", "The ultimate Mockoon alternative. Unblock your frontend team and speed up development.", "Create a local or cloud API mock server in seconds based on your OpenAPI specifications.", "Stop waiting for backend APIs. Simulate advanced API responses and test UIs faster."]
    )
    
    # 3. Multi-Protocol
    create_full_ad_group(
        'Google-Sa-Testing-Global', 'Testing-Multi-Protocol',
        ['test websocket api online', 'websocket client tool', 'grpc client online', 'test graphql api local', '[altair graphql client alternative]', '[bloomrpc alternative]', 'grpc gui client', 'test graphql mutations'],
        'https://apidog.com/blog/websocket-testing-tools/',
        ["Test WebSocket APIs Easily", "Best GraphQL Client Tool", "Advanced gRPC API Testing", "Beyond REST APIs", "Multi-Protocol API Client", "Test WebSockets Online", "Best gRPC GUI Client", "Visual GraphQL API Tester", "Debug APIs Flawlessly", "Support WebSockets & gRPC", "All-in-One API Tool", "Test Any API Protocol", "Powerful API Debugger", "Seamless API Testing", "Try Apidog for Free Today"],
        ["The ultimate API client for all protocols. Debug WebSocket, GraphQL, and gRPC endpoints.", "Stop using different tools for different APIs. Test REST, SOAP, and gRPC in one workspace.", "A powerful visual client for WebSocket and GraphQL testing. Elevate your workflow today.", "Easily connect, test, and debug multi-protocol APIs with an intuitive GUI. Start for free."]
    )
    print("\n>>> All Section 3 Deployments Completed Successfully!")
