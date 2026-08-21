import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

# Setup proxy for REST transport
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 2. RSA Ad Group Configuration with Dedicated Scenario Landing Pages
RSA_GROUPS_CONFIG = {
    "Enterprise-Compliance-Migration": {
        "campaign": "Google-Sa-Postman-Global",
        "final_url": "https://apidog.com/postman-alternative/",
        "tracking_suffix": "utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}",
        "keywords": [
            "postman enterprise alternative",
            "hipaa compliant api client",
            "soc2 compliant postman alternative",
            "postman offline mode for enterprise"
        ],
        "headlines": [
            "Postman Enterprise Alternative",
            "SOC2 & HIPAA Compliant Tool",
            "100% Local-First API Client",
            "No Mandatory Cloud Data Sync",
            "1-Click Postman Data Migration",
            "Offline-First API Workspace",
            "Secure Team API Collaboration",
            "No Postman Seat Limits",
            "Enterprise API Platform",
            "Keep API Data 100% Private",
            "Self-Hosted & Local Data",
            "Try Apidog Enterprise Free"
        ],
        "descriptions": [
            "Looking for a SOC2 and HIPAA compliant API client? Keep your API data 100% local.",
            "Migrate your Postman collections to Apidog effortlessly with full offline privacy.",
            "Eliminate Postman cloud data leakage risks. Secure, enterprise-grade API testing platform.",
            "All-in-one API client, automated testing & mock server for security-conscious dev teams."
        ]
    },
    "MCP-Debug-Tools": {
        "campaign": "Google-Sa-MCP-Infrastructure",
        "final_url": "https://apidog.com/blog/apidog-cli-agent-api-documentation/",
        "tracking_suffix": "utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}",
        "keywords": [
            "mcp server testing tool",
            "model context protocol inspector",
            "test mcp tool api",
            "ai agent api debugger"
        ],
        "headlines": [
            "MCP Server Testing & Debugging",
            "Model Context Protocol Tooling",
            "Test & Mock AI Agent APIs",
            "Inspect MCP Tool Endpoints",
            "Real-Time MCP Server Inspector",
            "AI Agent API Testing Platform",
            "Debug Anthropic MCP Servers",
            "Mock LLM Tool Responses",
            "Automate MCP Schema Tests",
            "Visual MCP API Debugger",
            "Fast MCP Tool Call Testing",
            "Try Apidog MCP Tools Free"
        ],
        "descriptions": [
            "Debug and test Model Context Protocol (MCP) servers effortlessly. Inspect LLM tool calls.",
            "Streamline your AI Agent development pipeline. Advanced API debugging & mock servers.",
            "Simulate MCP tool responses, test JSON schemas, and automate AI agent API testing.",
            "Visual debugger for Anthropic MCP and LLM tool APIs. Accelerate AI development today."
        ]
    },
    "API-Security-Testing": {
        "campaign": "Google-Sa-Testing-Global",
        "final_url": "https://apidog.com/api-testing/",
        "tracking_suffix": "utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}",
        "keywords": [
            "api security testing tool",
            "owasp api top 10 tester",
            "api vulnerability scanner",
            "jwt api security test"
        ],
        "headlines": [
            "API Security & Vulnerability",
            "OWASP API Top 10 Testing Tool",
            "Test JWT & Rate Limit Rules",
            "API Authentication Scanner",
            "DevSecOps API Security Testing",
            "Automated API Vulnerabilities",
            "Detect API BOLA & BFLA Flaws",
            "Validate API Auth Headers",
            "Secure Rest API Testing",
            "API Penetration Testing",
            "Continuous API Security",
            "Try Apidog Security Testing"
        ],
        "descriptions": [
            "Scan your APIs for OWASP Top 10 vulnerabilities, authentication bugs, and rate limits.",
            "Integrate API security checks directly into your developer workflow with zero setup.",
            "Detect broken object-level authorization (BOLA) and invalid tokens before deployment.",
            "All-in-one API testing platform with built-in security, schema validation & automated CI."
        ]
    },
    "Newman-Alternatives": {
        "campaign": "Google-Sa-CLI-Global",
        "final_url": "https://apidog.com/blog/lightweight-cli-tools-api-testing/",
        "tracking_suffix": "utm_source=google_search&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}",
        "keywords": [
            "newman cli alternative",
            "faster substitute for newman",
            "cli tool for api mocking",
            "headless api testing tool"
        ],
        "headlines": [
            "Fast Newman CLI Alternative",
            "Headless API Test Runner",
            "Run API Tests in CI/CD",
            "5x Faster CLI API Testing",
            "Apidog CLI Test Automation",
            "GitHub Actions API Runner",
            "GitLab CI/CD API Testing",
            "Terminal API Mock & Test",
            "Replace Slow Newman CLI",
            "Command Line API Debugger",
            "Automated Terminal Testing",
            "Try Apidog CLI For Free"
        ],
        "descriptions": [
            "Tired of slow Newman runs? Execute lightweight CLI API tests 5x faster in CI/CD pipelines.",
            "Run headless API regression tests and mock servers directly from your terminal.",
            "Native CLI runner for Apidog. Generate HTML reports and run tests on git push.",
            "Blazing fast CLI API testing tool for GitHub Actions, GitLab CI, and Bitbucket."
        ]
    }
}

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        ad_group_service = client.get_service("AdGroupService")
        ad_group_ad_service = client.get_service("AdGroupAdService")
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return

    # Fetch Ad Groups
    query = "SELECT ad_group.id, ad_group.name FROM ad_group WHERE ad_group.status = 'ENABLED'"
    ag_map = {}
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                ag_map[row.ad_group.name] = row.ad_group.id
    except Exception as e:
        print(f"Error querying ad groups: {e}")
        return

    for ag_name, config in RSA_GROUPS_CONFIG.items():
        if ag_name in ag_map:
            ag_id = ag_map[ag_name]
            ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, ag_id)

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

            try:
                response = ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=[ad_op])
                print(f"✅ Updated RSA Ad for '{ag_name}' with Final URL: {config['final_url']}")
            except Exception as e:
                print(f"Note/Notice for '{ag_name}': {e}")

if __name__ == "__main__":
    main()
