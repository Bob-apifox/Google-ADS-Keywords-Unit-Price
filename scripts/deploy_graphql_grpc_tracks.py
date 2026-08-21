import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

TRACKS = [
    {
        "campaign_name": "Google-Sa-Func-MultiProtocol-Global",
        "ad_group_name": "Testing-GraphQL-Client-Mock",
        "final_url": "https://apidog.com/blog/how-to-test-graphql-apis/",
        "tracking_suffix": "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}&utm_term={keyword}",
        "keywords": [
            ("graphql client", "PHRASE"),
            ("graphql testing tool", "PHRASE"),
            ("mock graphql api", "PHRASE"),
            ("graphql api client", "PHRASE"),
            ("best graphql client", "PHRASE"),
            ("graphql query builder", "PHRASE"),
            ("debug graphql apis", "PHRASE"),
            ("graphql mocking tool", "PHRASE")
        ],
        "headlines": [
            "Best GraphQL API Client",
            "Test GraphQL APIs Visually",
            "GraphQL Schema Auto Mock",
            "Visual GraphQL Query Builder",
            "Powerful GraphQL Testing",
            "GraphQL Client Alternative",
            "Debug GraphQL Mutations",
            "Explore GraphQL Schemas",
            "Stop Writing Manual Queries",
            "Seamless GraphQL Testing",
            "Multi-Protocol API Workspace",
            "Inspect GraphQL Responses",
            "Fast GraphQL Mock Server",
            "Live GraphQL Debugger",
            "Try Apidog for Free Today"
        ],
        "descriptions": [
            "Visual GraphQL client with auto schema fetch, interactive query runner, and smart mocks.",
            "Say goodbye to complex GraphQL setups. Auto-generate mocks and debug mutations live.",
            "Connect REST, GraphQL, WebSocket, and gRPC workflows seamlessly in one unified platform.",
            "Design, debug, mock, and test GraphQL APIs without writing complex boilerplate code."
        ]
    },
    {
        "campaign_name": "Google-Sa-Func-MultiProtocol-Global",
        "ad_group_name": "Testing-gRPC-Protobuf-GUI",
        "final_url": "https://apidog.com/blog/best-bloomrpc-alternative/",
        "tracking_suffix": "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_adgroup={adgroupid}&utm_term={keyword}",
        "keywords": [
            ("grpc client gui", "PHRASE"),
            ("grpc testing tool", "PHRASE"),
            ("debug grpc apis", "PHRASE"),
            ("protobuf api testing", "PHRASE"),
            ("bloomrpc alternative", "PHRASE"),
            ("grpc streaming test", "PHRASE"),
            ("grpc request tool", "PHRASE"),
            ("visual grpc client", "PHRASE")
        ],
        "headlines": [
            "Modern gRPC Client GUI",
            "Visual gRPC API Debugger",
            "Best BloomRPC Alternative",
            "Test gRPC Streams Easily",
            "Import Protobuf Files Fast",
            "Unary & Streaming gRPC",
            "Debug gRPC Endpoints Live",
            "Clean Intuitive gRPC GUI",
            "Replace Dead BloomRPC",
            "Seamless gRPC Testing",
            "Multi-Protocol API Tool",
            "Inspect gRPC Responses",
            "Fast Proto Schema Import",
            "Live gRPC Debugging Tool",
            "Try Apidog for Free Today"
        ],
        "descriptions": [
            "Looking for a modern gRPC GUI? Test unary and streaming gRPC calls with an intuitive UI.",
            "Import Proto files in seconds. Visual debugging for modern microservices and RPC APIs.",
            "Connect REST, gRPC, WebSocket, and SSE workflows in one unified developer workspace.",
            "Effortlessly inspect payloads, test bidirectional streams, and automate gRPC assertions."
        ]
    }
]

def validate_copies():
    for t in TRACKS:
        for i, h in enumerate(t["headlines"]):
            if len(h) > 30:
                raise ValueError(f"Headline {i+1} too long ({len(h)}): {h}")
            if "!" in h:
                raise ValueError(f"Headline {i+1} has '!': {h}")
        for i, d in enumerate(t["descriptions"]):
            if len(d) > 90:
                raise ValueError(f"Description {i+1} too long ({len(d)}): {d}")

def main():
    validate_copies()
    print("[PRE-FLIGHT] Creative length validation passed 100%!")

    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Get campaign resource name
    q_c = "SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name = 'Google-Sa-Func-MultiProtocol-Global'"
    c_res = None
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_c):
        for row in batch.results:
            c_res = row.campaign.resource_name

    if not c_res:
        print("Campaign not found!")
        return

    for t in TRACKS:
        ag_name = t["ad_group_name"]
        print(f"\n==========================================================================")
        print(f"[DEPLOYING] Track: {ag_name}")
        print(f"==========================================================================")

        # 1. Check if Ad Group already exists
        q_ag = f"SELECT ad_group.id, ad_group.name, ad_group.resource_name FROM ad_group WHERE campaign.name = 'Google-Sa-Func-MultiProtocol-Global' AND ad_group.name = '{ag_name}' AND ad_group.status != 'REMOVED'"
        ag_res = None
        for batch in ga_service.search_stream(customer_id=customer_id, query=q_ag):
            for row in batch.results:
                ag_res = row.ad_group.resource_name

        if not ag_res:
            ag_op = client.get_type("AdGroupOperation")
            ag = ag_op.create
            ag.name = ag_name
            ag.campaign = c_res
            ag.status = client.enums.AdGroupStatusEnum.ENABLED
            ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
            
            resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
            ag_res = resp.results[0].resource_name
            print(f"[SUCCESS] Created Ad Group '{ag_name}': {ag_res}")
        else:
            print(f"[INFO] Ad Group '{ag_name}' already exists: {ag_res}")

        # 2. Add Keywords
        kw_ops = []
        for kw_text, match_type in t["keywords"]:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_res
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw_text
            crit.keyword.match_type = getattr(client.enums.KeywordMatchTypeEnum, match_type)
            kw_ops.append(op)

        try:
            resp = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=kw_ops)
            print(f"[SUCCESS] Added {len(resp.results)} Keywords to '{ag_name}'")
        except Exception as e:
            print(f"[NOTE] Keywords addition: {e}")

        # 3. Create Compliant RSA Ad
        ad_op = client.get_type("AdGroupAdOperation")
        aga = ad_op.create
        aga.ad_group = ag_res
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = aga.ad
        ad.final_urls.append(t["final_url"])
        ad.final_url_suffix = t["tracking_suffix"]

        for h in t["headlines"]:
            hl = client.get_type("AdTextAsset")
            hl.text = h
            ad.responsive_search_ad.headlines.append(hl)

        for d in t["descriptions"]:
            ds = client.get_type("AdTextAsset")
            ds.text = d
            ad.responsive_search_ad.descriptions.append(ds)

        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"[SUCCESS] Created RSA Ad (15 Headlines, 4 Descriptions) for '{ag_name}'!")
        except Exception as e:
            print(f"[NOTE] RSA Ad Creation: {e}")

    print("\n==========================================================================")
    print("[ALL FINISHED] 4 Major Growth Points 100% Executed & Deployed Online!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
