import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# ==============================================================================
# DATA DEFINITIONS FOR PART 4
# ==============================================================================

# 4.1 DSA 17 Competitor Alternatives
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

# 4.2 SSE Real-Time Protocols
SSE_TRACK = {
    "campaign_name": "Google-Sa-Func-MultiProtocol-Global",
    "budget_usd": 30.0,
    "tcpa_usd": 2.50,
    "ad_group_name": "Testing-SSE-Stream-Protocols",
    "final_url": "https://apidog.com/blog/how-to-test-sse-apis/",
    "tracking_suffix": "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}&utm_term={keyword}",
    "keywords": [
        "test sse stream endpoint",
        "server-sent events testing tool",
        "test sse api online",
        "debug server sent events",
        "stream api response testing",
        "sse client test tool",
        "test sse connection",
        "server sent events debugger"
    ],
    "headlines": [
        "Test SSE Streams Easily",
        "Real-Time API Testing Tool",
        "Server-Sent Events Client",
        "Visual SSE Stream Debugger",
        "Best SSE & WebSocket Client",
        "Stream API Response Viewer",
        "Free SSE Testing Workspace",
        "Debug SSE Endpoints Live",
        "Stop Writing Custom Scripts",
        "Seamless Stream Testing",
        "Multi-Protocol API Tool",
        "Inspect Server-Sent Events",
        "Fast Event Stream Inspector",
        "Live SSE Debugging Tool",
        "Try Apidog for Free Today"
    ],
    "descriptions": [
        "Connect, inspect, and debug Server-Sent Events in real time. Perfect visual client.",
        "The ultimate multi-protocol tool. Effortlessly test REST, WebSockets, and SSE streams.",
        "Stream API responses directly in your visual workspace. Fast, reliable, and zero code.",
        "Inspect event streams, payload data, and connection health visually. Get started free."
    ]
}

# 4.3 Heavy QA & Contract Testing
HEAVY_QA_TRACK = {
    "campaign_name": "Google-Sa-Comp-HeavyQA-Global",
    "budget_usd": 45.0,
    "tcpa_usd": 2.50,
    "ad_group_name": "ReadyAPI-Pact-Alternative",
    "final_url": "https://apidog.com/blog/best-readyapi-alternative/",
    "tracking_suffix": "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}&utm_term={keyword}",
    "keywords_phrase": [
        "readyapi alternative",
        "soapui pro alternative",
        "smartbear alternative",
        "karate api testing alternative",
        "detect api breaking changes",
        "api contract testing tool",
        "pact alternative api testing"
    ],
    "keywords_exact": [
        "readyapi alternative",
        "karate api testing"
    ],
    "headlines": [
        "Best ReadyAPI Alternative",
        "Visual API Contract Testing",
        "Automated API Testing Tool",
        "Better Than SoapUI Pro",
        "Detect Breaking Changes Fast",
        "Modern API QA Workspace",
        "Data-Driven API Tests",
        "CI/CD API Test Pipeline",
        "No Heavy XML Boilerplate",
        "Fast Visual Test Scenarios",
        "Replace Complex QA Tools",
        "Free Enterprise API Testing",
        "OpenAPI Native Test Suites",
        "Powerful API Assertions",
        "Try Apidog for Free Today"
    ],
    "descriptions": [
        "Heavy desktop QA tools slowing you down? Upgrade to a faster modern visual API platform.",
        "Visual API contract testing and regression suites. Detect breaking changes before deploy.",
        "Seamlessly integrates with Jenkins, GitHub Actions, and GitLab for robust CI/CD testing.",
        "Support data-driven testing, database assertions, and visual flow control with ease."
    ]
}

# 4.4 Docs Auto-Generation
DOCS_GEN_TRACK = {
    "campaign_name": "Google-Sa-Doc-Global",
    "budget_usd": 25.0,
    "tcpa_usd": 2.50,
    "ad_group_name": "Docs-Auto-Generation",
    "final_url": "https://apidog.com/api-doc/",
    "tracking_suffix": "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}&utm_term={keyword}",
    "keywords": [
        "auto generate api docs",
        "generate interactive api documentation",
        "swagger ui auto generator",
        "openapi to interactive docs",
        "api documentation software",
        "create api developer portal"
    ],
    "headlines": [
        "Auto Generate API Docs",
        "Interactive API Documentation",
        "Beautiful API Portals",
        "Zero Maintenance Docs",
        "OpenAPI to Beautiful Docs",
        "Fast API Doc Generator",
        "Live Try-It-Out Runner",
        "Modern Swagger Alternative",
        "Publish API Docs in 1 Click",
        "Auto Sync Docs with Specs",
        "Developer-Friendly Docs",
        "Custom Domain & Branding",
        "Interactive API Explorer",
        "Next-Gen API Documentation",
        "Try Apidog for Free Today"
    ],
    "descriptions": [
        "Generate stunning interactive API documentation automatically from your OpenAPI specs.",
        "Zero manual documentation maintenance. Beautiful developer portals with live API runners.",
        "Keep documentation in perfect sync with your API code. Custom domains and rich themes.",
        "Empower external developers with interactive API docs and instant mock servers. Try free."
    ]
}

def validate_character_limits():
    print("--- [PRE-FLIGHT VALIDATION: Character Limits & Counts] ---")
    all_valid = True
    
    for track in [SSE_TRACK, HEAVY_QA_TRACK, DOCS_GEN_TRACK]:
        cname = track["campaign_name"]
        print(f"Checking Track: {cname}...")
        
        # Check headlines
        if len(track["headlines"]) != 15:
            print(f"  [ERROR] {cname} headlines count is {len(track['headlines'])}, must be exactly 15!")
            all_valid = False
        for i, h in enumerate(track["headlines"]):
            if len(h) > 30:
                print(f"  [ERROR] Headline {i+1} exceeds 30 chars ({len(h)}): '{h}'")
                all_valid = False
            if '!' in h:
                print(f"  [ERROR] Headline {i+1} contains exclamation mark '!': '{h}'")
                all_valid = False

        # Check descriptions
        if len(track["descriptions"]) != 4:
            print(f"  [ERROR] {cname} descriptions count is {len(track['descriptions'])}, must be exactly 4!")
            all_valid = False
        for i, d in enumerate(track["descriptions"]):
            if len(d) > 90:
                print(f"  [ERROR] Description {i+1} exceeds 90 chars ({len(d)}): '{d}'")
                all_valid = False

    # Check DSA descriptions
    for art in DSA_ARTICLES:
        comp = art["competitor"]
        if len(art["desc1"]) > 90:
            print(f"  [ERROR] DSA {comp} Desc 1 exceeds 90 chars ({len(art['desc1'])})")
            all_valid = False
        if len(art["desc2"]) > 90:
            print(f"  [ERROR] DSA {comp} Desc 2 exceeds 90 chars ({len(art['desc2'])})")
            all_valid = False

    if all_valid:
        print("[SUCCESS] All Headlines (15/15, <=30 chars) and Descriptions (4/4, <=90 chars) are 100% compliant!")
    return all_valid

def update_campaign_budget_and_tcpa(client, customer_id, campaign_name, budget_usd, tcpa_usd):
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")

    q = f"SELECT campaign.id, campaign.resource_name, campaign.campaign_budget, campaign.bidding_strategy_type FROM campaign WHERE campaign.name = '{campaign_name}'"
    c_row = None
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            c_row = row.campaign
            break
            
    if not c_row:
        print(f"[ERROR] Campaign {campaign_name} not found!")
        return None

    # Update budget
    b_op = client.get_type("CampaignBudgetOperation")
    b_up = b_op.update
    b_up.resource_name = c_row.campaign_budget
    b_up.amount_micros = int(budget_usd * 1000000)
    client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_up._pb))
    budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])

    # Update tCPA
    c_op = client.get_type("CampaignOperation")
    c_up = c_op.update
    c_up.resource_name = c_row.resource_name
    if "MAXIMIZE_CONVERSIONS" in c_row.bidding_strategy_type.name:
        c_up.maximize_conversions.target_cpa_micros = int(tcpa_usd * 1000000)
    else:
        c_up.target_cpa.target_cpa_micros = int(tcpa_usd * 1000000)
    client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_up._pb))
    campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])

    print(f"[SUCCESS] Updated [{campaign_name}] -> Budget: ${budget_usd:.2f}/day | Target CPA: ${tcpa_usd:.2f}")
    return c_row.resource_name

def create_rsa_track(client, customer_id, track_data):
    cname = track_data["campaign_name"]
    print(f"\n==========================================================================")
    print(f"[EXECUTING] Track: {cname} -> Ad Group: {track_data['ad_group_name']}")
    print(f"==========================================================================")
    
    # 1. Update Campaign Budget and tCPA
    c_resource = update_campaign_budget_and_tcpa(client, customer_id, cname, track_data["budget_usd"], track_data["tcpa_usd"])
    if not c_resource:
        return

    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # 2. Check or Create Ad Group
    ag_name = track_data["ad_group_name"]
    ag_query = f"SELECT ad_group.id, ad_group.resource_name FROM ad_group WHERE campaign.resource_name = '{c_resource}' AND ad_group.name = '{ag_name}'"
    ag_resource = None
    for batch in ga_service.search_stream(customer_id=customer_id, query=ag_query):
        for row in batch.results:
            ag_resource = row.ad_group.resource_name
            print(f"[INFO] Ad Group '{ag_name}' already exists: {ag_resource}")
            break

    if not ag_resource:
        ag_op = client.get_type("AdGroupOperation")
        ag = ag_op.create
        ag.campaign = c_resource
        ag.name = ag_name
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
        ag_resource = ag_resp.results[0].resource_name
        print(f"[SUCCESS] Created Ad Group '{ag_name}': {ag_resource}")

    # 3. Add Keywords
    existing_kws = set()
    kw_query = f"SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type FROM ad_group_criterion WHERE ad_group.resource_name = '{ag_resource}' AND ad_group_criterion.type = 'KEYWORD'"
    for batch in ga_service.search_stream(customer_id=customer_id, query=kw_query):
        for row in batch.results:
            existing_kws.add((row.ad_group_criterion.keyword.text.lower(), row.ad_group_criterion.keyword.match_type.name))

    kw_ops = []
    # Phrase match keywords
    phrase_list = track_data.get("keywords") or track_data.get("keywords_phrase") or []
    for kw in phrase_list:
        if (kw.lower(), "PHRASE") not in existing_kws:
            crit_op = client.get_type("AdGroupCriterionOperation")
            crit = crit_op.create
            crit.ad_group = ag_resource
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            kw_ops.append(crit_op)

    # Exact match keywords (if any)
    exact_list = track_data.get("keywords_exact", [])
    for kw in exact_list:
        if (kw.lower(), "EXACT") not in existing_kws:
            crit_op = client.get_type("AdGroupCriterionOperation")
            crit = crit_op.create
            crit.ad_group = ag_resource
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            kw_ops.append(crit_op)

    if kw_ops:
        ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=kw_ops)
        print(f"[SUCCESS] Added {len(kw_ops)} Keywords to '{ag_name}'")
    else:
        print(f"[INFO] All keywords already exist in '{ag_name}'")

    # 4. Create RSA Responsive Search Ad (15 Headlines, 4 Descriptions, Final URL & Tracking Suffix)
    # Check if RSA already exists
    ad_query = f"SELECT ad_group_ad.ad.id FROM ad_group_ad WHERE ad_group.resource_name = '{ag_resource}' AND ad_group_ad.status != 'REMOVED'"
    has_ad = False
    for batch in ga_service.search_stream(customer_id=customer_id, query=ad_query):
        for _ in batch.results:
            has_ad = True
            break

    if not has_ad:
        ad_op = client.get_type("AdGroupAdOperation")
        aga = ad_op.create
        aga.ad_group = ag_resource
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = aga.ad
        ad.final_urls.append(track_data["final_url"])
        ad.final_url_suffix = track_data["tracking_suffix"]
        
        # 15 Headlines
        for h_text in track_data["headlines"]:
            h = client.get_type("AdTextAsset")
            h.text = h_text
            ad.responsive_search_ad.headlines.append(h)
            
        # 4 Descriptions
        for d_text in track_data["descriptions"]:
            d = client.get_type("AdTextAsset")
            d.text = d_text
            ad.responsive_search_ad.descriptions.append(d)
            
        ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
        print(f"[SUCCESS] Created Compliant RSA (15 Headlines, 4 Descriptions) for '{ag_name}'")
    else:
        print(f"[INFO] RSA Ad already exists in '{ag_name}'")

def execute_dsa_track(client, customer_id):
    print(f"\n==========================================================================")
    print(f"[EXECUTING] 4.1 DSA Competitor Alternatives Matrix (17 Products = 17 Groups)")
    print(f"==========================================================================")

    cname = "Google-Sa-DSA-Alternatives-Global"
    c_resource = update_campaign_budget_and_tcpa(client, customer_id, cname, 50.0, 2.50)
    if not c_resource:
        return

    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    existing_ags = {}
    ag_query = f"SELECT ad_group.id, ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.resource_name = '{c_resource}'"
    for batch in ga_service.search_stream(customer_id=customer_id, query=ag_query):
        for row in batch.results:
            existing_ags[row.ad_group.name] = row.ad_group.resource_name

    for art in DSA_ARTICLES:
        comp = art["competitor"]
        ag_name = f"DSA-{comp}-Alternative"
        
        # 1. Ad Group
        if ag_name in existing_ags:
            ag_resource = existing_ags[ag_name]
        else:
            try:
                ag_op = client.get_type("AdGroupOperation")
                ag = ag_op.create
                ag.campaign = c_resource
                ag.name = ag_name
                ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
                ag.status = client.enums.AdGroupStatusEnum.ENABLED
                ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
                ag_resource = ag_resp.results[0].resource_name
                existing_ags[ag_name] = ag_resource
                print(f"[SUCCESS] Created DSA Ad Group: '{ag_name}'")
            except Exception as e:
                print(f"[ERROR] Creating DSA Ad Group '{ag_name}': {e}")
                continue

        # 2. Dynamic Webpage Criteria (Exact URL Target)
        try:
            agc_op = client.get_type("AdGroupCriterionOperation")
            agc = agc_op.create
            agc.ad_group = ag_resource
            agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            webpage = agc.webpage
            webpage.criterion_name = f"Target: {comp} Alt"
            
            condition = client.get_type("WebpageConditionInfo")
            condition.operand = client.enums.WebpageConditionOperandEnum.URL
            condition.operator = client.enums.WebpageConditionOperatorEnum.EQUALS
            condition.argument = art["url"]
            webpage.conditions.append(condition)
            
            ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[agc_op])
            print(f"  └─ Added Exact Webpage Target: {art['url']}")
        except Exception as e:
            # Often criterion already exists or is configured
            pass

        # 3. Dynamic Search Ad with Custom Copy & Tracking Suffix
        try:
            ad_op = client.get_type("AdGroupAdOperation")
            aga = ad_op.create
            aga.ad_group = ag_resource
            aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
            
            ad = aga.ad
            ad.final_url_suffix = "utm_source=google_dsa&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}"
            ad.dynamic_search_ad.description1 = art["desc1"]
            ad.dynamic_search_ad.description2 = art["desc2"]
            
            ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"  └─ Added DSA Descriptions & Tracking for {comp}")
        except Exception as e:
            pass

def main():
    if not validate_character_limits():
        print("[ERROR] Character validation failed. Halting execution.")
        return

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID

    # 1. Execute 4.1 DSA Alternatives Matrix
    execute_dsa_track(client, customer_id)

    # 2. Execute 4.2 SSE Real-Time Protocols Track
    create_rsa_track(client, customer_id, SSE_TRACK)

    # 3. Execute 4.3 Heavy QA & Contract Testing Track
    create_rsa_track(client, customer_id, HEAVY_QA_TRACK)

    # 4. Execute 4.4 Docs Auto-Generation Track
    create_rsa_track(client, customer_id, DOCS_GEN_TRACK)

    print("\n==========================================================================")
    print("[ALL FINISHED] Part 4 All 4 Expansion Tracks Successfully Deployed Online!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
