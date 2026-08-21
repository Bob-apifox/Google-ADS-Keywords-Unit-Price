import os
import sys
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

TRACKING_SUFFIX = "utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

RSA_GROUPS_CONFIG = {
    "AI-Agent-Orchestration": {
        "campaign": "Google-Sa-Solutions-AI-LLM-Global",
        "final_url": "https://apidog.com/blog/apidog-cli-agent-api-documentation/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "ai agent workflow debugger",
            "function calling test tool",
            "langchain api test framework",
            "llamaindex api mock server"
        ],
        "headlines": [
            "AI Agent API Debugging",
            "Test Function Calling APIs",
            "LangChain & LlamaIndex Tools",
            "Inspect LLM Tool Responses",
            "Real-Time AI Agent Debugger",
            "Mock AI Tool Call Outputs",
            "Automate AI Agent Workflow",
            "Test MCP & Agent Frameworks",
            "Visual Agent API Test Bench",
            "Fast AI Schema Validation",
            "Debug Complex LLM Pipelines",
            "Try Apidog AI Tools Free"
        ],
        "descriptions": [
            "Debug and test AI Agent function calling APIs. Inspect LLM tool responses in real time.",
            "Streamline your AI workflow. Advanced API debugging, mock servers & automated testing.",
            "Simulate AI Agent tool outputs, validate JSON schemas, and test LangChain endpoints.",
            "All-in-one API workspace for AI engineers. Accelerate LLM agent development today."
        ]
    },
    "Realtime-SSE-Streaming": {
        "campaign": "Google-Sa-Func-MultiProtocol-Global",
        "final_url": "https://apidog.com/api-debugging/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "test sse stream endpoint",
            "websocket mock server online",
            "realtime eventstream debugger",
            "debug chatgpt sse response"
        ],
        "headlines": [
            "Test SSE Stream Endpoints",
            "WebSocket API Client Online",
            "Debug Real-Time API Streams",
            "Inspect EventStream Responses",
            "LLM Response Streaming Test",
            "Fast WebSocket Debugger",
            "Test Server-Sent Events",
            "Live SSE Connection Tester",
            "Multi-Protocol API Debugger",
            "Realtime API Mock & Test",
            "Debug Streaming Endpoints",
            "Try Apidog Streaming Tools"
        ],
        "descriptions": [
            "Test Server-Sent Events (SSE) and WebSocket streams easily. Inspect real-time data flow.",
            "Debug LLM response streaming and eventstream APIs with zero configuration needed.",
            "Simulate WebSocket servers, test SSE endpoints, and debug streaming APIs in Apidog.",
            "Powerful multi-protocol API client for REST, WebSocket, SSE, GraphQL, and gRPC."
        ]
    },
    "Postman-Privacy-LocalFirst": {
        "campaign": "Google-Sa-Postman-Global",
        "final_url": "https://apidog.com/postman-alternative/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "postman local data privacy",
            "postman alternative offline desktop",
            "postman collection runner alternative",
            "free postman alternative for teams"
        ],
        "headlines": [
            "Postman Local Data Privacy",
            "Offline-First Postman Sub",
            "No Mandatory Cloud Sync",
            "100% Local API Workspace",
            "1-Click Postman Import",
            "Free Desktop API Client",
            "No Collection Runner Limit",
            "SOC2 & HIPAA Compliant Tool",
            "Secure Team API Testing",
            "Replace Cloud-Only Postman",
            "Keep Your API Specs Private",
            "Try Apidog Local-First"
        ],
        "descriptions": [
            "Protect your API data with 100% local-first storage. No forced cloud synchronization.",
            "Looking for an offline Postman alternative? Keep collections secure on your machine.",
            "Migrate from Postman in 1-click. Unlimited collection runner executions for free.",
            "Enterprise-grade local API client with built-in mocking, documentation, and testing."
        ]
    },
    "Smart-Mock-Server": {
        "campaign": "Google-Sa-Mock-Global",
        "final_url": "https://apidog.com/api-mocking/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "mock server for frontend teams",
            "generate json mock api online",
            "fast mock api endpoint generator",
            "local mock server for rest api"
        ],
        "headlines": [
            "Smart Mock Server Generator",
            "Mock APIs for Frontend Teams",
            "Generate JSON Mock Endpoints",
            "Fast Local Mock Server",
            "Zero-Code API Mocking",
            "Simulate API Latency & Error",
            "Dynamic Mock Data Engine",
            "Unblock Frontend Dev Fast",
            "Auto Mock JSON Responses",
            "Faker JS Data Generator",
            "Online Mock Server Free",
            "Try Apidog Mock Server"
        ],
        "descriptions": [
            "Create dynamic mock API endpoints in seconds. Unblock frontend development effortlessly.",
            "Generate realistic mock JSON responses based on your OpenAPI or JSON schema rules.",
            "Simulate slow networks, HTTP 500 errors, and custom response logic without code.",
            "All-in-one local and online mock server for modern software engineering teams."
        ]
    }
}

CAMPAIGN_NEGATIVES = {
    "Google-Sa-Doc-Global": [
        "pdf generator", "free template", "word doc", "google doc", "excel"
    ],
    "Google-Sa-Stoplight-Global": [
        "stoplight traffic", "studio source", "red light", "traffic light"
    ],
    "Google-Sa-Insomnia-Global": [
        "insomnia treatment", "sleep disorder", "medication", "cure"
    ],
    "Google-Sa-Mock-Global": [
        "mockup design", "ui mockup", "figma mockup", "photoshop"
    ]
}

GLOBAL_NEGATIVES = [
    "ai coding", "ai prompt", "ai writer", "ai bot", "ai generator code", "llm price", "how to build ai",
    "crack", "free download pdf", "student discount", "course", "tutorial for beginners", "job vacancy", "medical doc", "sleep", "minecraft"
]

DSA_TARGETS_CONFIG = {
    "DSA-Mock-Group": {
        "campaign": "Google-Sa-DSA-Global",
        "urls": [
            "https://apidog.com/api-mocking/",
            "https://apidog.com/blog/best-mock-api-tools/",
            "https://apidog.com/blog/mock-server-guide/",
            "https://apidog.com/blog/mock-api-for-frontend-testing/"
        ]
    }
}

def main():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        campaign_service = client.get_service("CampaignService")
        ad_group_service = client.get_service("AdGroupService")
        ad_group_ad_service = client.get_service("AdGroupAdService")
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
        campaign_criterion_service = client.get_service("CampaignCriterionService")
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return

    # Map Campaign Name -> Campaign ID
    campaign_map = {}
    print(">>> Fetching enabled campaigns...")
    query_campaigns = "SELECT campaign.id, campaign.name FROM campaign WHERE campaign.status = 'ENABLED'"
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_campaigns)
        for batch in stream:
            for row in batch.results:
                campaign_map[row.campaign.name] = row.campaign.id
    except Exception as e:
        print(f"Error fetching campaigns: {e}")
        return

    def get_or_create_ad_group(c_name, ag_name):
        c_id = campaign_map.get(c_name)
        if not c_id:
            print(f"WARNING: Campaign '{c_name}' not found.")
            return None
            
        query = f"SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.id = {c_id} AND ad_group.name = '{ag_name}' AND ad_group.status != 'REMOVED'"
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
            for batch in stream:
                for row in batch.results:
                    print(f"Found existing Ad Group '{ag_name}' (ID: {row.ad_group.id})")
                    return row.ad_group.id
        except Exception as e:
            print(f"Error querying ad group '{ag_name}': {e}")

        op = client.get_type("AdGroupOperation")
        ag = op.create
        ag.campaign = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        ag.name = ag_name
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ag.tracking_url_template = "{lpurl}?" + TRACKING_SUFFIX

        try:
            response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[op])
            new_id = response.results[0].resource_name.split('/')[-1]
            print(f"SUCCESS: Created new Ad Group '{ag_name}' with Tracking Suffix (ID: {new_id})")
            return new_id
        except Exception as e:
            print(f"Error creating ad group '{ag_name}': {e}")
            return None

    print("\n>>> Building July 22 Incremental Ad Groups, Keywords & RSA Ads...")
    for ag_name, config in RSA_GROUPS_CONFIG.items():
        ag_id = get_or_create_ad_group(config["campaign"], ag_name)
        if not ag_id:
            continue

        ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)

        # Keywords
        kw_ops = []
        for kw_text in config["keywords"]:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_path
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw_text
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
            kw_ops.append(op)

        if kw_ops:
            try:
                response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
                print(f"Added {len(response.results)} keywords to '{ag_name}'")
            except Exception as e:
                print(f"Notice adding keywords: {e}")

        # RSA Ad with Tracking Suffix
        ad_op = client.get_type("AdGroupAdOperation")
        ag_ad = ad_op.create
        ag_ad.ad_group = ag_path
        ag_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        rsa = ag_ad.ad.responsive_search_ad
        for hl in config["headlines"]:
            text_asset = client.get_type("AdTextAsset")
            text_asset.text = hl
            rsa.headlines.append(text_asset)

        for desc in config["descriptions"]:
            text_asset = client.get_type("AdTextAsset")
            text_asset.text = desc
            rsa.descriptions.append(text_asset)

        ag_ad.ad.final_urls.append(config["final_url"])
        ag_ad.ad.tracking_url_template = "{lpurl}?" + config["tracking_suffix"]
        ag_ad.ad.final_url_suffix = config["tracking_suffix"]

        try:
            response = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
            print(f"SUCCESS: Created RSA Ad with Tracking Suffix for '{ag_name}' ({config['final_url']})")
        except Exception as e:
            print(f"Notice creating RSA ad for '{ag_name}': {e}")

    # Add Campaign Negative Keywords
    print("\n>>> Deploying Campaign Negative Keywords...")
    for c_name, neg_list in CAMPAIGN_NEGATIVES.items():
        c_id = campaign_map.get(c_name)
        if not c_id:
            continue
        c_path = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        neg_ops = []
        for neg_text in neg_list:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = c_path
            crit.negative = True
            crit.keyword.text = neg_text
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
            neg_ops.append(op)
        
        try:
            response = campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=neg_ops)
            print(f"✅ Deployed {len(response.results)} campaign negative keywords to '{c_name}'")
        except Exception as e:
            print(f"Notice deploying campaign negatives for '{c_name}': {e}")

    # Add DSA targets
    print("\n>>> Adding DSA Webpage Targets...")
    for ag_name, config in DSA_TARGETS_CONFIG.items():
        query_ag = f"SELECT ad_group.id FROM ad_group WHERE campaign.name = '{config['campaign']}' AND ad_group.name = '{ag_name}' AND ad_group.status != 'REMOVED'"
        try:
            stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ag)
            dsa_ag_id = None
            for batch in stream:
                for row in batch.results:
                    dsa_ag_id = row.ad_group.id
                    break
            
            if dsa_ag_id:
                ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, dsa_ag_id)
                target_ops = []
                for url in config["urls"]:
                    op = client.get_type("AdGroupCriterionOperation")
                    crit = op.create
                    crit.ad_group = ag_path
                    crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                    
                    webpage_condition = client.get_type("WebpageConditionInfo")
                    webpage_condition.operand = client.enums.WebpageConditionOperandEnum.URL
                    webpage_condition.argument = url
                    
                    crit.webpage.criterion_name = f"Exact URL: {url[:30]}"
                    crit.webpage.conditions.append(webpage_condition)
                    target_ops.append(op)

                response = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=target_ops)
                print(f"SUCCESS: Bound {len(response.results)} Webpage URLs to DSA Ad Group '{ag_name}'")
        except Exception as e:
            print(f"Notice adding DSA targets: {e}")

    print("\n🎉 JULY 22 INCREMENTAL PLAN PREPARED AND READY!")

if __name__ == "__main__":
    main()
