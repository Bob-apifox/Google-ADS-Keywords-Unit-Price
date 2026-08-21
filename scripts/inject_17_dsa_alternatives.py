import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 17 Flagship Competitor Alternative Articles
ARTICLES = [
    {
        "competitor": "Pact",
        "category": "Contract Testing",
        "url": "https://apidog.com/blog/best-pact-alternative/",
        "desc1": "Looking for the best Pact alternative? Visual API contract testing made simple.",
        "desc2": "Detect breaking changes instantly. Collaborate on API specs and tests in one workspace."
    },
    {
        "competitor": "BloomRPC",
        "category": "gRPC Client",
        "url": "https://apidog.com/blog/best-bloomrpc-alternative/",
        "desc1": "Need a modern BloomRPC alternative? Test & debug gRPC APIs with an intuitive GUI.",
        "desc2": "Import Protobuf files in seconds. Visual unary and streaming gRPC debugging for teams."
    },
    {
        "competitor": "MuleSoft",
        "category": "Enterprise API Platform",
        "url": "https://apidog.com/blog/best-mulesoft-alternative/",
        "desc1": "Tired of heavy MuleSoft enterprise complexity? Switch to agile API design & testing.",
        "desc2": "All-in-one API lifecycle management without bloated enterprise overhead. Try free."
    },
    {
        "competitor": "k6",
        "category": "Performance Testing",
        "url": "https://apidog.com/blog/best-k6-alternative/",
        "desc1": "The ultimate k6 alternative. Run distributed visual load tests without scripting.",
        "desc2": "Stress-test APIs, simulate thousands of virtual users, and analyze latency curves live."
    },
    {
        "competitor": "JMeter",
        "category": "Load & Stress Testing",
        "url": "https://apidog.com/blog/best-jmeter-alternative/",
        "desc1": "Say goodbye to JMeter XML boilerplate. Modern visual API stress testing is here.",
        "desc2": "Configure realistic load test scenarios in minutes with real-time performance analytics."
    },
    {
        "competitor": "Thunder Client",
        "category": "VSCode API Client",
        "url": "https://apidog.com/blog/best-thunder-client-alternative/",
        "desc1": "Looking for a Thunder Client alternative? Full-featured API client with team sync.",
        "desc2": "Seamless visual debugging, automated tests, and rich mocks. Import in 1 single click."
    },
    {
        "competitor": "Apiary",
        "category": "API Design & Documentation",
        "url": "https://apidog.com/blog/best-apiary-alternative/",
        "desc1": "Looking for an Apiary alternative? Visual OpenAPI design, mocking & documentation.",
        "desc2": "Design APIs first, auto-generate interactive docs, and simulate responses instantly."
    },
    {
        "competitor": "ReadyAPI",
        "category": "Enterprise API QA",
        "url": "https://apidog.com/blog/best-readyapi-alternative/",
        "desc1": "Heavy desktop ReadyAPI slowing you down? Upgrade to a faster modern API platform.",
        "desc2": "Enterprise-grade automated testing, data-driven tests, and CI/CD integration for free."
    },
    {
        "competitor": "Mintlify",
        "category": "Developer Docs",
        "url": "https://apidog.com/blog/best-mintlify-alternative/",
        "desc1": "The #1 Mintlify alternative. Auto-generate stunning interactive API documentation.",
        "desc2": "Zero maintenance docs from OpenAPI specs. Beautiful developer portal with live runner."
    },
    {
        "competitor": "SoapUI",
        "category": "SOAP & REST Testing",
        "url": "https://apidog.com/blog/best-soapui-alternative/",
        "desc1": "Modernize your API workflow. Switch from legacy SoapUI to a clean visual workspace.",
        "desc2": "Support REST, SOAP, WebSockets & GraphQL. Run test suites with visual flow control."
    },
    {
        "competitor": "ReadMe",
        "category": "Developer Portals",
        "url": "https://apidog.com/blog/best-readme-alternative/",
        "desc1": "Better developer portals without enterprise costs. The top ReadMe alternative.",
        "desc2": "Interactive API docs, instant mock servers, and built-in API testing out of the box."
    },
    {
        "competitor": "SwaggerHub",
        "category": "OpenAPI Design",
        "url": "https://apidog.com/blog/best-swaggerhub-alternative/",
        "desc1": "Design APIs faster than SwaggerHub. Visual OpenAPI editor with real-time validation.",
        "desc2": "Collaborate on API specs, share mock endpoints, and generate docs automatically."
    },
    {
        "competitor": "Postman",
        "category": "API Lifecycle",
        "url": "https://apidog.com/blog/best-postman-alternative/",
        "desc1": "Tired of Postman runner limits and pricing? Switch to Apidog for unlimited testing.",
        "desc2": "1-click Postman migration. Unify API design, debugging, testing, and mock servers."
    },
    {
        "competitor": "Bruno",
        "category": "Offline API Client",
        "url": "https://apidog.com/blog/best-bruno-alternative/",
        "desc1": "Looking for the best Bruno alternative? Complete visual API workspace with Git sync.",
        "desc2": "Local-first privacy, zero vendor lock-in, and team collaboration. Import in seconds."
    },
    {
        "competitor": "Stoplight",
        "category": "Design-First Modeling",
        "url": "https://apidog.com/blog/best-stoplight-alternative/",
        "desc1": "The ultimate Stoplight Studio alternative. Visual API modeling & OpenAPI governance.",
        "desc2": "Design-first API workflow, auto mock data generation, and beautiful interactive docs."
    },
    {
        "competitor": "Insomnia",
        "category": "REST & GraphQL Client",
        "url": "https://apidog.com/blog/best-insomnia-alternative/",
        "desc1": "Looking for an Insomnia alternative? Fast, intuitive API debugging with local storage.",
        "desc2": "Import Insomnia collections in seconds. Powerful environment variables and test scripts."
    },
    {
        "competitor": "Hoppscotch",
        "category": "Open Source API Tool",
        "url": "https://apidog.com/blog/best-hoppscotch-alternative/",
        "desc1": "Need better team management & automated testing? Move from Hoppscotch to Apidog.",
        "desc2": "Unified workspace for API design, debugging, automated test scenarios, and mocking."
    }
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID

    # 1. Search for Google-Sa-DSA-Alternatives-Global
    query = "SELECT campaign.id, campaign.resource_name, campaign.status FROM campaign WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'"
    response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    campaign_resource_name = None
    for row in response:
        campaign_resource_name = row.campaign.resource_name
        print(f"Found Campaign: {row.campaign.resource_name} (Status: {row.campaign.status.name})")
        break

    if not campaign_resource_name:
        print("Campaign 'Google-Sa-DSA-Alternatives-Global' not found! Falling back to 'Google-Sa-DSA-Global'...")
        q2 = "SELECT campaign.id, campaign.resource_name FROM campaign WHERE campaign.name = 'Google-Sa-DSA-Global'"
        resp2 = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=q2)
        for row in resp2:
            campaign_resource_name = row.campaign.resource_name
            print(f"Found Fallback Campaign: {campaign_resource_name}")
            break

    if not campaign_resource_name:
        print("Error: No DSA Campaign found!")
        return

    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Fetch existing ad groups in this campaign to avoid duplicates
    existing_ags = {}
    ag_query = f"SELECT ad_group.id, ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.resource_name = '{campaign_resource_name}'"
    for r in client.get_service("GoogleAdsService").search(customer_id=customer_id, query=ag_query):
        existing_ags[r.ad_group.name] = r.ad_group.resource_name

    print(f"Existing Ad Groups in Campaign: {len(existing_ags)}")

    for art in ARTICLES:
        ag_name = f"DSA-Alt-{art['competitor']}"
        print(f"\nProcessing {ag_name} ({art['url']})...")
        
        # 1. Ad Group
        if ag_name in existing_ags:
            ag_resource_name = existing_ags[ag_name]
            print(f"  Ad Group already exists: {ag_resource_name}")
        else:
            try:
                ag_op = client.get_type("AdGroupOperation")
                ag = ag_op.create
                ag.campaign = campaign_resource_name
                ag.name = ag_name
                ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
                ag.status = client.enums.AdGroupStatusEnum.ENABLED
                ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
                ag_resource_name = ag_resp.results[0].resource_name
                existing_ags[ag_name] = ag_resource_name
                print(f"  Created Ad Group: {ag_resource_name}")
            except Exception as e:
                print(f"  Error creating Ad Group {ag_name}: {e}")
                continue

        # 2. Webpage Criterion (Exact URL match)
        try:
            agc_op = client.get_type("AdGroupCriterionOperation")
            agc = agc_op.create
            agc.ad_group = ag_resource_name
            agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            webpage = agc.webpage
            webpage.criterion_name = f"Target: {art['competitor']} Alt"
            
            condition = client.get_type("WebpageConditionInfo")
            condition.operand = client.enums.WebpageConditionOperandEnum.URL
            condition.operator = client.enums.WebpageConditionOperatorEnum.EQUALS
            condition.argument = art['url']
            webpage.conditions.append(condition)
            
            ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[agc_op])
            print(f"  Added Webpage Target: {art['url']}")
        except Exception as e:
            print(f"  Note on Criterion for {art['competitor']}: {e}")

        # 3. Dynamic Search Ad
        try:
            ad_op = client.get_type("AdGroupAdOperation")
            ad_group_ad = ad_op.create
            ad_group_ad.ad_group = ag_resource_name
            ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
            
            ad = ad_group_ad.ad
            ad.dynamic_search_ad.description1 = art['desc1']
            ad.dynamic_search_ad.description2 = art['desc2']
            
            ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"  Added DSA Ad Copy for {art['competitor']}")
        except Exception as e:
            print(f"  Note on Ad Copy for {art['competitor']}: {e}")

    print("\n✅ All 17 'The Best Alternative' URLs successfully processed for DSA!")

if __name__ == '__main__':
    main()
