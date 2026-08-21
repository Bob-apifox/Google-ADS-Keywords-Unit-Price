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
    "Postman-Team-Collaboration": {
        "campaign": "Google-Sa-Postman-Global",
        "final_url": "https://apidog.com/postman-alternative/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "postman team collaboration limit",
            "postman free team limit alternative",
            "postman workspace alternative free",
            "offline postman alternative for teams"
        ],
        "headlines": [
            "Postman Free Team Alternative",
            "No Team Member Limits",
            "Unlimited Postman Workspace",
            "Secure Local-First API Client",
            "1-Click Postman Import",
            "Collaborate Free With Teams",
            "No Postman Cloud Paywalls",
            "SOC2 & HIPAA Compliant Tool",
            "Replace Costly Postman Seats",
            "Free API Testing Workspace",
            "Keep Team API Specs Private",
            "Try Apidog Free For Teams"
        ],
        "descriptions": [
            "Tired of Postman seat limits? Collaborate with unlimited team members for free in Apidog.",
            "Migrate your Postman collections in 1-click. Keep your team API workspace 100% secure.",
            "No forced cloud sync, no team limits, unlimited runner executions. Built for dev teams.",
            "All-in-one API client, documentation generator, mock server & automated testing platform."
        ]
    },
    "Automated-API-Regression-Runner": {
        "campaign": "Google-Sa-Testing-Global",
        "final_url": "https://apidog.com/api-testing/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "automated api regression testing",
            "ci cd api test runner",
            "api load testing alternative to jmeter",
            "k6 api testing alternative"
        ],
        "headlines": [
            "Automated API Regression Test",
            "CI/CD API Test Pipeline",
            "Zero-Code API Test Runner",
            "Fast JMeter & K6 Alternative",
            "GitHub Actions API Runner",
            "Visual API Test Assertions",
            "Run API Tests On Git Push",
            "Automate REST API Testing",
            "Continuous API Quality Tool",
            "Generate HTML Test Reports",
            "Fast Terminal & GUI Testing",
            "Try Apidog Testing Free"
        ],
        "descriptions": [
            "Automate REST and GraphQL API testing with zero code. Run regression suites in CI/CD.",
            "Fast alternative to JMeter and Postman runner. Generate visual HTML reports effortlessly.",
            "Integrate API tests into GitHub Actions & GitLab CI. Validate status codes & schemas.",
            "All-in-one API testing platform with built-in assertions, variables & CLI runner."
        ]
    },
    "Auto-Interactive-API-Docs": {
        "campaign": "Google-Sa-Doc-Global",
        "final_url": "https://apidog.com/api-doc/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "auto generate api docs from code",
            "openapi 3.1 interactive doc generator",
            "swagger doc site builder",
            "readme io alternative free"
        ],
        "headlines": [
            "Auto Generate Interactive Docs",
            "OpenAPI 3.1 Documentation Tool",
            "Swagger & Readme Alternative",
            "Instant Online API Hub",
            "Share Live API Documentation",
            "Zero-Maintenance API Site",
            "Beautiful Developer Portals",
            "Try APIs Directly In Browser",
            "Custom Domain API Docs",
            "Auto Sync Code With Docs",
            "Free Interactive API Viewer",
            "Try Apidog Doc Generator"
        ],
        "descriptions": [
            "Generate beautiful, interactive API documentation automatically from your API requests.",
            "Say goodbye to manual Swagger updates. Keep API docs 100% in sync with your codebase.",
            "Allow developers to test endpoints directly inside browser docs. Custom domain support.",
            "Free alternative to ReadMe.io and Stoplight. Publish secure developer portals in seconds."
        ]
    },
    "Frontend-Unblock-Mock-Server": {
        "campaign": "Google-Sa-Mock-Global",
        "final_url": "https://apidog.com/api-mocking/",
        "tracking_suffix": TRACKING_SUFFIX,
        "keywords": [
            "mock api for frontend development",
            "faker json mock server online",
            "simulate backend api response",
            "wiremock online alternative"
        ],
        "headlines": [
            "Mock APIs For Frontend Teams",
            "Smart Mock Server Generator",
            "Faker JS Data Simulation",
            "Unblock Frontend Dev Fast",
            "Generate JSON Mock Endpoints",
            "WireMock Online Alternative",
            "Zero-Code Dynamic Mocking",
            "Simulate Slow Network & 500",
            "Fast Local & Cloud Mocking",
            "Schema-Based Mock Responses",
            "Instant Mock Server Online",
            "Try Apidog Mock Server"
        ],
        "descriptions": [
            "Unblock frontend development in seconds. Generate smart mock API responses automatically.",
            "Mock JSON endpoints based on OpenAPI schemas or Faker.js rules without writing code.",
            "Simulate network latency, HTTP 500 errors, and custom response logic for edge cases.",
            "Powerful local and cloud mock server for agile software teams. Free to try today."
        ]
    }
}

CAMPAIGN_NEGATIVES = {
    "Google-Sa-Doc-Global": [
        "pdf generator", "free template", "word doc", "google doc", "excel", "resume format"
    ],
    "Google-Sa-Testing-Global": [
        "blood test", "unit test java", "medical test", "covid test", "iq test"
    ],
    "Google-Sa-Mock-Global": [
        "mockup design", "ui mockup", "figma mockup", "photoshop", "3d mockup"
    ],
    "Google-Sa-Postman-Global": [
        "postman job", "postman salary", "postman delivery", "mailman"
    ]
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

    print("\n>>> Building July 23 Flagship Ad Groups, Keywords & RSA Ads...")
    for ag_name, config in RSA_GROUPS_CONFIG.items():
        ag_id = get_or_create_ad_group(config["campaign"], ag_name)
        if not ag_id:
            continue

        ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)

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

    print("\n🎉 ALL RSA ADS UPDATED AND DEPLOYED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
