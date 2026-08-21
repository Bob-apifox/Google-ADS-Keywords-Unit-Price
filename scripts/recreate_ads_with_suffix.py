import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
ad_group_ad_service = client.get_service("AdGroupAdService")
customer_id = '9496728294'

suffix_str = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

ad_groups_data = {
    'API-Docs-Generation': {
        'final_url': 'https://apidog.com/api-doc/',
        'headlines': ["Best API Documentation Tool", "Beautiful API Documentation", "Auto-Generate API Docs", "Interactive API Docs", "Stop Syncing Docs Manually", "Swagger UI Alternative", "Better Than Redoc", "OpenAPI to Docs Instantly", "Zero Code API Documentation", "Share APIs with Your Team", "Professional API Portal", "Free API Documentation Tool", "#1 API Design Platform", "Seamless API Collaboration", "Try Apidog for Free Today"],
        'descriptions': ["Stop syncing docs manually. Generate interactive API docs instantly from OpenAPI specs.", "Build a beautiful, customized API developer portal in minutes. Try Apidog for free.", "The ultimate alternative to Swagger UI and Redoc. Auto-generate docs from your code.", "Enhance developer experience with beautiful, interactive, and shareable documentation."]
    },
    'Mock-Server-Frontend': {
        'final_url': 'https://apidog.com/api-mocking/',
        'headlines': ["Smart API Mock Server", "Best Mockoon Alternative", "Fake REST API Generator", "Unblock Your Frontend Team", "Generate Mock Data Instantly", "Local API Mocking Tool", "Better Than JSON Server", "Open Source Mock Server", "Dynamic Mock API Data", "Zero-Code Mocking Engine", "OpenAPI to Mock Server", "Start Mocking APIs for Free", "Frontend Development Tool", "Simulate API Responses", "Try Apidog for Free Today"],
        'descriptions': ["Generate dynamic fake data instantly without writing backend code. 100% realistic.", "The ultimate Mockoon alternative. Unblock your frontend team and speed up development.", "Create a local or cloud API mock server in seconds based on your OpenAPI specifications.", "Stop waiting for backend APIs. Simulate advanced API responses and test UIs faster."]
    },
    'Testing-Multi-Protocol': {
        'final_url': 'https://apidog.com/blog/websocket-testing-tools/',
        'headlines': ["Test WebSocket APIs Easily", "Best GraphQL Client Tool", "Advanced gRPC API Testing", "Beyond REST APIs", "Multi-Protocol API Client", "Test WebSockets Online", "Best gRPC GUI Client", "Visual GraphQL API Tester", "Debug APIs Flawlessly", "Support WebSockets & gRPC", "All-in-One API Tool", "Test Any API Protocol", "Powerful API Debugger", "Seamless API Testing", "Try Apidog for Free Today"],
        'descriptions': ["The ultimate API client for all protocols. Debug WebSocket, GraphQL, and gRPC endpoints.", "Stop using different tools for different APIs. Test REST, SOAP, and gRPC in one workspace.", "A powerful visual client for WebSocket and GraphQL testing. Elevate your workflow today.", "Easily connect, test, and debug multi-protocol APIs with an intuitive GUI. Start for free."]
    }
}

q = """
    SELECT ad_group_ad.ad.id, ad_group.id, ad_group.name, ad_group.resource_name
    FROM ad_group_ad
    WHERE ad_group.name IN ('API-Docs-Generation', 'Mock-Server-Frontend', 'Testing-Multi-Protocol')
"""

stream = ga_service.search_stream(customer_id=customer_id, query=q)

remove_ops = []
recreate_ag_resources = {}

for batch in stream:
    for row in batch.results:
        # Create REMOVE operation
        op = client.get_type('AdGroupAdOperation')
        op.remove = ad_group_ad_service.ad_group_ad_path(customer_id, row.ad_group.id, row.ad_group_ad.ad.id)
        remove_ops.append(op)
        # Store resource_name for recreation
        recreate_ag_resources[row.ad_group.name] = row.ad_group.resource_name

if remove_ops:
    print(f"Removing {len(remove_ops)} existing ads...")
    ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=remove_ops)

create_ops = []
for ag_name, ag_res in recreate_ag_resources.items():
    data = ad_groups_data[ag_name]
    op = client.get_type("AdGroupAdOperation")
    ad = op.create
    ad.ad_group = ag_res
    ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    # Correct fields!
    ad.ad.final_urls.append(data['final_url'])
    ad.ad.final_url_suffix = suffix_str
    
    for h in data['headlines']:
        asset = client.get_type("AdTextAsset")
        asset.text = h
        ad.ad.responsive_search_ad.headlines.append(asset)
    for d in data['descriptions']:
        asset = client.get_type("AdTextAsset")
        asset.text = d
        ad.ad.responsive_search_ad.descriptions.append(asset)
        
    create_ops.append(op)

if create_ops:
    print(f"Recreating {len(create_ops)} ads with final_url_suffix...")
    resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=create_ops)
    print(f"Successfully recreated {len(resp.results)} ads.")
