import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

# 🎯 精准一脉相承的定制参数（告别一刀切，每系列量身定制）
EXACT_ADJUSTMENTS = {
    "Google-Sa-Jmeter-Global": {
        "budget_usd": 95.0,
        "tcpa_usd": 1.50, # 从 $0.84 放宽至 $1.50（7天实际 $1.40）
        "reason": "放开 $0.84 限制，允许以 $1.50 吸收增量负载测试流量"
    },
    "Google-Sa-Hoppscotch-Global": {
        "budget_usd": 45.0,
        "tcpa_usd": 1.60, # 从 $0.88 放宽至 $1.60（7天实际 $1.60）
        "reason": "解开 $0.88 严重限流瓶颈，让其吃满 $45 预算"
    },
    "Google-Sa-Fern-Global": {
        "budget_usd": 48.0,
        "tcpa_usd": 1.80, # 从 $0.84 放宽至 $1.80（7天实际 $1.74）
        "reason": "匹配 $1.74 真实转化水平，扩大现代 API 团队获客"
    },
    "Google-Sa-Readme-Global": {
        "budget_usd": 75.0,
        "tcpa_usd": 1.80, # 维持精准的 $1.80（7天实际 $1.79）
        "reason": "当前 $1.80 tCPA 运行极佳，纯加大预算至 $75 放大规模"
    },
    "Google-Sa-API Editor-Global": {
        "budget_usd": 32.0,
        "tcpa_usd": 1.80, # 维持健康的 $1.80（7天实际 $1.54）
        "reason": "维持 $1.80 良好出价，日预算提升至 $32 放大出单"
    },
    "Google-Sa-Func-MultiProtocol-Global": {
        "budget_usd": 30.0,
        "tcpa_usd": 1.80, # 设为 $1.80（7天实际 $1.28）
        "reason": "给 SSE 实时协议组充足竞价空间，预算提升至 $30"
    },
    "Google-Sa-Bruno-Global": {
        "budget_usd": 15.0,
        "tcpa_usd": 2.00, # 维持 $2.00（7天实际 $1.62）
        "reason": "维持 $2.00 出价，预算翻倍至 $15 抢占离线市场"
    },
    "Google-Sa-Comp-HeavyQA-Global": {
        "budget_usd": 45.0,
        "tcpa_usd": 1.60, # 设为 $1.60（7天实际 $1.09）
        "reason": "ReadyAPI 表现超神，预算加至 $45 扩大收割"
    }
}

def apply_adjustments(dry_run=True):
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")

    print(f"=== {'[DRY RUN PREVIEW]' if dry_run else '[EXECUTING LIVE CHANGES]'} ===")
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.resource_name,
            campaign.campaign_budget,
            campaign.bidding_strategy_type,
            campaign.maximize_conversions.target_cpa_micros,
            campaign.target_cpa.target_cpa_micros
        FROM campaign
        WHERE campaign.name IN ({', '.join([f"'{c}'" for c in EXACT_ADJUSTMENTS.keys()])})
    """

    for batch in ga_service.search_stream(customer_id=customer_id, query=query):
        for row in batch.results:
            c = row.campaign
            name = c.name
            adj = EXACT_ADJUSTMENTS[name]
            
            # 1. Budget Operation
            new_budget_micros = int(adj["budget_usd"] * 1000000)
            b_op = client.get_type("CampaignBudgetOperation")
            b_update = b_op.update
            b_update.resource_name = c.campaign_budget
            b_update.amount_micros = new_budget_micros
            client.copy_from(b_op.update_mask, protobuf_helpers.field_mask(None, b_update._pb))

            # 2. Campaign Target CPA Operation
            new_tcpa_micros = int(adj["tcpa_usd"] * 1000000)
            c_op = client.get_type("CampaignOperation")
            c_update = c_op.update
            c_update.resource_name = c.resource_name
            if "MAXIMIZE_CONVERSIONS" in c.bidding_strategy_type.name:
                c_update.maximize_conversions.target_cpa_micros = new_tcpa_micros
            else:
                c_update.target_cpa.target_cpa_micros = new_tcpa_micros
            client.copy_from(c_op.update_mask, protobuf_helpers.field_mask(None, c_update._pb))

            print(f"[{name}] (ID: {c.id})")
            print(f"  ├─ Budget:    -> ${adj['budget_usd']:.2f}/day")
            print(f"  ├─ Target CPA: -> ${adj['tcpa_usd']:.2f}")
            print(f"  └─ Strategy:  {adj['reason']}")

            if not dry_run:
                try:
                    budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
                    campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
                    print("  ✅ Applied successfully!")
                except Exception as e:
                    print(f"  ❌ Error applying changes: {e}")

if __name__ == '__main__':
    # Default to Preview/Dry Run. Call with False to execute live.
    apply_adjustments(dry_run=True)
