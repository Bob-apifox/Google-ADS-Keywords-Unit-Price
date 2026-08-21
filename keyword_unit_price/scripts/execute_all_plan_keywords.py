import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient

# Setup proxy for REST transport
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = "d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml"
CUSTOMER_ID = "9496728294"

# Full 60+ Keywords Matrix from optimization_plan_2026-07-20.md
ALL_KEYWORDS_MAPPING = {
    "Google-Sa-Postman-Global": {
        "Postman-Performance-Pain-Global": [
            "postman collection runner limit",
            "postman cloud sync issues",
            "postman offline mode workaround",
            "postman login restriction"
        ],
        "Postman Alternative-Global": [
            "app like postman",
            "tools like postman",
            "postman alternative no login",
            "postman runner limit alternative",
            "postman team collaboration cost"
        ],
        "Enterprise-Compliance-Migration": [
            "postman enterprise alternative",
            "hipaa compliant api client",
            "soc2 compliant postman alternative",
            "postman offline mode for enterprise"
        ]
    },
    "Google-Sa-SpecFirst-Global": {
        "Stoplight-Alternative": [
            "stoplight studio alternatives open source",
            "swagger editor alternative free",
            "openapi visual editor like stoplight"
        ]
    },
    "Google-Sa-Insomnia-Global": {
        "insomnia api-Global": [
            "insomnia sync collections team",
            "soapui rest testing framework",
            "insomnia offline alternative desktop"
        ]
    },
    "Google-Sa-Testing-Global": {
        "Automated api testing, Global": [
            "ci cd api testing",
            "api testing pipeline",
            "automated rest api tests",
            "continuous api testing"
        ],
        "API-Security-Testing": [
            "api security testing tool",
            "owasp api top 10 tester",
            "api vulnerability scanner",
            "jwt api security test"
        ]
    },
    "Google-Sa-Doc-Global": {
        "api-document-Global": [
            "auto generate api docs",
            "interactive api docs",
            "openapi 3.1 doc generator",
            "share api specs online"
        ]
    },
    "Google-Sa-Mock-Global": {
        "Mock Global": [
            "dynamic mock server",
            "fake api endpoint generator",
            "local mock server json",
            "simulate api errors"
        ]
    },
    "Google-Sa-Func-CICD-Global": {
        "API-Pipeline": [
            "github actions api testing",
            "gitlab ci api mock server",
            "run api tests on git push"
        ]
    },
    "Google-Sa-Category-Competitor-Global": {
        "Category-Competitor": [
            "free api tool for teams",
            "open source api client desktop",
            "self hosted api documentation",
            "offline first api testing tool"
        ]
    },
    "Google-Sa-Comp-VSCode-Global": {
        "Thunder-Client & REST-Client": [
            "vscode api client plugin",
            "rest client vscode alternative",
            "thunder client free limit alternative",
            "test apis directly in vscode"
        ]
    },
    "Google-Sa-CLI-Global": {
        "Newman-Alternatives": [
            "newman cli alternative",
            "faster substitute for newman",
            "cli tool for api mocking",
            "headless api testing tool"
        ]
    },
    "Google-Sa-MCP-Infrastructure": {
        "MCP-Debug-Tools": [
            "mcp server testing tool",
            "model context protocol inspector",
            "test mcp tool api",
            "ai agent api debugger"
        ]
    },
    "Google-Sa-Func-MultiProtocol-Global": {
        "WebSocket-SSE": [
            "sse endpoint testing tool",
            "websocket api client online",
            "debug sse stream api",
            "realtime api debugging tool"
        ],
        "GraphQL-gRPC": [
            "graphql api client online",
            "grpc testing tool free"
        ]
    },
    "Google-Sa-Solutions-API-First-Global": {
        "JSON Schema Tooling": [
            "typespec visual editor",
            "openapi 3.1 gui editor",
            "api contract testing tool",
            "detect api breaking changes"
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
        campaign_service = client.get_service("CampaignService")
        ad_group_service = client.get_service("AdGroupService")
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    except Exception as e:
        print(f"Failed to load Google Ads client: {e}")
        return

    # Query all active campaigns and ad groups
    campaign_ag_map = {}
    print(">>> Querying active campaigns & ad groups...")
    query = """
        SELECT
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.type
        FROM ad_group
        WHERE campaign.status = 'ENABLED'
          AND ad_group.status = 'ENABLED'
    """
    try:
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        for batch in stream:
            for row in batch.results:
                c_name = row.campaign.name
                ag_name = row.ad_group.name
                ag_id = row.ad_group.id
                ag_type = row.ad_group.type.name
                
                if c_name not in campaign_ag_map:
                    campaign_ag_map[c_name] = {}
                campaign_ag_map[c_name][ag_name] = {"id": ag_id, "type": ag_type}
    except Exception as e:
        print(f"Error querying campaigns & ad groups: {e}")
        return

    total_added = 0
    total_skipped = 0

    print("\n>>> Processing full 60+ keywords injection across all campaigns...")
    for c_name, ag_dict in ALL_KEYWORDS_MAPPING.items():
        if c_name not in campaign_ag_map:
            # Check for alternative campaign name matching
            matched_c_name = None
            for active_c in campaign_ag_map.keys():
                if c_name.replace("API-First", "APT-First") == active_c or active_c.startswith(c_name[:15]):
                    matched_c_name = active_c
                    break
            if matched_c_name:
                c_name = matched_c_name
            else:
                print(f"WARNING: Campaign '{c_name}' not found or disabled. Skipping.")
                continue

        active_ag_dict = campaign_ag_map[c_name]
        
        for ag_target_name, kw_list in ag_dict.items():
            target_ag_id = None
            
            # Find matching ad group or fallback to first SEARCH_STANDARD ad group
            if ag_target_name in active_ag_dict:
                target_ag_id = active_ag_dict[ag_target_name]["id"]
            else:
                # Fallback matching
                for active_ag, info in active_ag_dict.items():
                    if info["type"] == "SEARCH_STANDARD":
                        target_ag_id = info["id"]
                        print(f"Notice: AdGroup '{ag_target_name}' mapped to active SEARCH_STANDARD AdGroup '{active_ag}' ({info['id']}) in Campaign '{c_name}'")
                        break
            
            if not target_ag_id:
                print(f"WARNING: No SEARCH_STANDARD AdGroup found in Campaign '{c_name}' for keywords {kw_list}")
                continue

            ag_path = ad_group_service.ad_group_path(CUSTOMER_ID, target_ag_id)
            operations = []
            for kw_text in kw_list:
                op = client.get_type("AdGroupCriterionOperation")
                crit = op.create
                crit.ad_group = ag_path
                crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                crit.keyword.text = kw_text
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
                operations.append(op)

            if operations:
                try:
                    response = ad_group_criterion_service.mutate_ad_group_criteria(
                        customer_id=CUSTOMER_ID, operations=operations
                    )
                    added_cnt = len(response.results)
                    total_added += added_cnt
                    print(f"✅ Campaign '{c_name}' -> AdGroup ID {target_ag_id}: Injected {added_cnt} keywords: {kw_list[:2]}...")
                except Exception as e:
                    print(f"Note/Notice adding keywords to '{c_name}' -> {ag_target_name}: {e}")

    print(f"\n🎉 EXHAUSTIVE KEYWORD INJECTION FINISHED! Total {total_added} keywords processed across all plan matrix sections.")

if __name__ == "__main__":
    main()
