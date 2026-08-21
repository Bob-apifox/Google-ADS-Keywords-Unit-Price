import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

DSA_ARTICLES = [
    {
        "competitor": "Pact",
        "url": "https://apidog.com/blog/best-pact-alternative/",
        "desc1": "Looking for the best Pact alternative? Visual API contract testing made simple.",
        "desc2": "Detect breaking changes instantly. Collaborate on API specs and tests in one workspace."
    },
    {
        "competitor": "BloomRPC",
        "url": "https://apidog.com/blog/best-bloomrpc-alternative/",
        "desc1": "Need a modern BloomRPC alternative? Test & debug gRPC APIs with an intuitive GUI.",
        "desc2": "Import Protobuf files in seconds. Visual unary and streaming gRPC debugging for teams."
    },
    {
        "competitor": "MuleSoft",
        "url": "https://apidog.com/blog/best-mulesoft-alternative/",
        "desc1": "Tired of heavy MuleSoft enterprise complexity? Switch to agile API design & testing.",
        "desc2": "All-in-one API lifecycle management without bloated enterprise overhead. Try free."
    },
    {
        "competitor": "k6",
        "url": "https://apidog.com/blog/best-k6-alternative/",
        "desc1": "The ultimate k6 alternative. Run distributed visual load tests without scripting.",
        "desc2": "Stress-test APIs, simulate thousands of virtual users, and analyze latency curves live."
    },
    {
        "competitor": "JMeter",
        "url": "https://apidog.com/blog/best-jmeter-alternative/",
        "desc1": "Say goodbye to JMeter XML boilerplate. Modern visual API stress testing is here.",
        "desc2": "Configure realistic load test scenarios in minutes with real-time performance analytics."
    },
    {
        "competitor": "ThunderClient",
        "url": "https://apidog.com/blog/best-thunder-client-alternative/",
        "desc1": "Looking for a Thunder Client alternative? Full-featured API client with team sync.",
        "desc2": "Seamless visual debugging, automated tests, and rich mocks. Import in 1 single click."
    },
    {
        "competitor": "Apiary",
        "url": "https://apidog.com/blog/best-apiary-alternative/",
        "desc1": "Looking for an Apiary alternative? Visual OpenAPI design, mocking & documentation.",
        "desc2": "Design APIs first, auto-generate interactive docs, and simulate responses instantly."
    },
    {
        "competitor": "ReadyAPI",
        "url": "https://apidog.com/blog/best-readyapi-alternative/",
        "desc1": "Heavy desktop ReadyAPI slowing you down? Upgrade to a faster modern API platform.",
        "desc2": "Enterprise-grade automated testing, data-driven tests, and CI/CD integration for free."
    },
    {
        "competitor": "Mintlify",
        "url": "https://apidog.com/blog/best-mintlify-alternative/",
        "desc1": "The #1 Mintlify alternative. Auto-generate stunning interactive API documentation.",
        "desc2": "Zero maintenance docs from OpenAPI specs. Beautiful developer portal with live runner."
    },
    {
        "competitor": "SoapUI",
        "url": "https://apidog.com/blog/best-soapui-alternative/",
        "desc1": "Modernize your API workflow. Switch from legacy SoapUI to a clean visual workspace.",
        "desc2": "Support REST, SOAP, WebSockets & GraphQL. Run test suites with visual flow control."
    },
    {
        "competitor": "ReadMe",
        "url": "https://apidog.com/blog/best-readme-alternative/",
        "desc1": "Better developer portals without enterprise costs. The top ReadMe alternative.",
        "desc2": "Interactive API docs, instant mock servers, and built-in API testing out of the box."
    },
    {
        "competitor": "SwaggerHub",
        "url": "https://apidog.com/blog/best-swaggerhub-alternative/",
        "desc1": "Design APIs faster than SwaggerHub. Visual OpenAPI editor with real-time validation.",
        "desc2": "Collaborate on API specs, share mock endpoints, and generate docs automatically."
    },
    {
        "competitor": "Postman",
        "url": "https://apidog.com/blog/best-postman-alternative/",
        "desc1": "Tired of Postman runner limits and pricing? Switch to Apidog for unlimited testing.",
        "desc2": "1-click Postman migration. Unify API design, debugging, testing, and mock servers."
    },
    {
        "competitor": "Bruno",
        "url": "https://apidog.com/blog/best-bruno-alternative/",
        "desc1": "Looking for the best Bruno alternative? Complete visual API workspace with Git sync.",
        "desc2": "Local-first privacy, zero vendor lock-in, and team collaboration. Import in seconds."
    },
    {
        "competitor": "Stoplight",
        "url": "https://apidog.com/blog/best-stoplight-alternative/",
        "desc1": "The ultimate Stoplight Studio alternative. Visual API modeling & OpenAPI governance.",
        "desc2": "Design-first API workflow, auto mock data generation, and beautiful interactive docs."
    },
    {
        "competitor": "Insomnia",
        "url": "https://apidog.com/blog/best-insomnia-alternative/",
        "desc1": "Looking for an Insomnia alternative? Fast, intuitive API debugging with local storage.",
        "desc2": "Import Insomnia collections in seconds. Powerful environment variables and test scripts."
    },
    {
        "competitor": "Hoppscotch",
        "url": "https://apidog.com/blog/best-hoppscotch-alternative/",
        "desc1": "Need better team management & automated testing? Move from Hoppscotch to Apidog.",
        "desc2": "Unified workspace for API design, debugging, automated test scenarios, and mocking."
    }
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    print("==========================================================================")
    print("[DEPLOYING] Dynamic Search Ads for All 17 Competitor Alternative Ad Groups")
    print("==========================================================================")

    # 1. Fetch all Ad Groups in Google-Sa-DSA-Alternatives-Global
    q = """
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.resource_name
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
          AND ad_group.status = 'ENABLED'
    """
    ad_groups = {}
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q):
        for row in batch.results:
            ad_groups[row.ad_group.name] = row.ad_group.resource_name

    # 2. Fetch existing enabled ads to avoid duplication
    ads_q = """
        SELECT
            ad_group.name,
            ad_group_ad.ad.id,
            ad_group_ad.status
        FROM ad_group_ad
        WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global'
          AND ad_group_ad.status = 'ENABLED'
    """
    existing_ads = set()
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=ads_q):
        for row in batch.results:
            existing_ads.add(row.ad_group.name)

    operations = []
    for art in DSA_ARTICLES:
        comp = art["competitor"]
        ag_name = f"DSA-{comp}-Alternative"
        
        if ag_name not in ad_groups:
            print(f"[WARN] Ad Group '{ag_name}' not found!")
            continue

        ag_resource = ad_groups[ag_name]
        
        if ag_name in existing_ads:
            print(f"[INFO] Ad Group '{ag_name}' already has an active Expanded DSA Ad.")
            continue

        # Create Expanded Dynamic Search Ad
        ad_op = client.get_type("AdGroupAdOperation")
        aga = ad_op.create
        aga.ad_group = ag_resource
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = aga.ad
        ad.final_url_suffix = "utm_source=google_dsa&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}"
        ad.expanded_dynamic_search_ad.description = art["desc1"]
        ad.expanded_dynamic_search_ad.description2 = art["desc2"]
        
        operations.append(ad_op)
        print(f"[QUEUED] Creating Expanded DSA Ad for '{ag_name}'...")
        print(f"  ├─ Desc 1: {art['desc1']}")
        print(f"  └─ Desc 2: {art['desc2']}")

    if operations:
        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=operations)
            print(f"\n[SUCCESS] Successfully deployed {len(resp.results)} Expanded Dynamic Search Ads!")
        except Exception as e:
            print(f"\n[ERROR] Failed to deploy ads: {e}")
    else:
        print("\n[INFO] All 17 Ad Groups already have active ads.")

    print("\n==========================================================================")
    print("[FINISHED] 17 DSA Ad Creatives Deployment Completed!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
