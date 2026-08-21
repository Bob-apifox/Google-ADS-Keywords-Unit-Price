import os
import sys
import time
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join(os.path.dirname(__file__), "../../common/config/google-ads.yaml")
CUSTOMER_ID = "9496728294"

def get_google_ads_client():
    for attempt in range(5):
        try:
            return GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        except Exception as e:
            print(f"Loading client attempt {attempt+1} failed: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to initialize Google Ads Client.")

def retry_api_call(func, description, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as e:
            print(f"⚠️ [{description}] 尝试 {attempt}/{max_retries} 失败: {e}")
            if attempt == max_retries:
                print(f"❌ [{description}] 最终失败，跳过。")
                return None
            time.sleep(2 * attempt)

def fetch_campaigns(client):
    ga_service = client.get_service("GoogleAdsService")
    c_query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.bidding_strategy_type,
            campaign.campaign_budget,
            campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    camps = {}
    def query_camps():
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=c_query)
        for batch in stream:
            for row in batch.results:
                c = row.campaign
                b = row.campaign_budget
                camps[c.name] = {
                    "id": str(c.id),
                    "budget_resource": c.campaign_budget,
                    "budget_amount": b.amount_micros / 1e6 if b.amount_micros else 0,
                    "bidding_type": c.bidding_strategy_type.name
                }
    retry_api_call(query_camps, "查询活跃 Campaign")
    return camps

def update_budgets_and_tcpa(client, camps_info, updates):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")
    
    print("\n==================================================")
    print("💰 执行 8月21日 预算调整与 Target CPA 精细化优化...")
    print("==================================================")
    
    for c_name, conf in updates.items():
        if c_name not in camps_info:
            print(f"⚠️ 未找到系列: {c_name}")
            continue
        info = camps_info[c_name]
        c_id = info["id"]
        budget_res = info["budget_resource"]
        new_budget = conf["budget_usd"]
        new_tcpa = conf["tcpa_usd"]
        
        # 1. Update Budget
        def do_update_budget():
            budget_op = client.get_type("CampaignBudgetOperation")
            budget = budget_op.update
            budget.resource_name = budget_res
            budget.amount_micros = int(new_budget * 1_000_000)
            budget_op.update_mask.paths.append("amount_micros")
            campaign_budget_service.mutate_campaign_budgets(
                customer_id=CUSTOMER_ID, operations=[budget_op]
            )
            print(f"✅ [{c_name}] 预算: ${info['budget_amount']} ➔ ${new_budget}/天")
            
        retry_api_call(do_update_budget, f"更新预算 [{c_name}]")
            
        # 2. Update Target CPA
        def do_update_tcpa():
            tcpa_op = client.get_type("CampaignOperation")
            camp = tcpa_op.update
            camp.resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
            bidding_type = info["bidding_type"]
            if bidding_type == "TARGET_CPA":
                camp.target_cpa.target_cpa_micros = int(new_tcpa * 1_000_000)
                tcpa_op.update_mask.paths.append("target_cpa.target_cpa_micros")
            else:
                camp.maximize_conversions.target_cpa_micros = int(new_tcpa * 1_000_000)
                tcpa_op.update_mask.paths.append("maximize_conversions.target_cpa_micros")
            campaign_service.mutate_campaigns(
                customer_id=CUSTOMER_ID, operations=[tcpa_op]
            )
            print(f"✅ [{c_name}] Target CPA ➔ ${new_tcpa}")

        retry_api_call(do_update_tcpa, f"更新Target CPA [{c_name}]")

def main():
    print("==================================================")
    print("🚀 Google Ads 8月21日精细化控盘与爆款加码执行器")
    print("==================================================")
    
    client = get_google_ads_client()
    camps_info = fetch_campaigns(client)
    print(f"✅ 成功加载 {len(camps_info)} 个活跃系列信息。")
    
    updates_21st = {
        "Google-Sa-Solutions-API-First-Global": {"budget_usd": 50.0, "tcpa_usd": 2.20}, # 重炮加码爆单黑马 ($1.80 单价)
        "Google-Sa-Expansion-Horizon-2026": {"budget_usd": 65.0, "tcpa_usd": 2.80},     # 预算与出价回调平稳
        "Google-Dis-DevPlacements-Global": {"budget_usd": 5.0, "tcpa_usd": 2.50},        # 压降展示白名单空耗 ($25.99/天 节省)
        "Google-Dis-Remarketing-Global": {"budget_usd": 5.0, "tcpa_usd": 2.50},          # 压降展示再营销空耗 ($10.96/天 节省)
        "Google-Sa-Category-Competitor-Global": {"budget_usd": 12.0, "tcpa_usd": 2.50}, # 压制高价刺客 ($27.16/单)
        "Google-Sa-Jmeter-Global": {"budget_usd": 35.0, "tcpa_usd": 2.80},              # 削减预算
        "Google-Sa-Mintlify-Global": {"budget_usd": 10.0, "tcpa_usd": 2.50},            # 削减预算
    }
    update_budgets_and_tcpa(client, camps_info, updates_21st)
    
    print("\n==================================================")
    print("🎉 [DONE] 8月21日 精细化控盘与爆款加码方案上线完成！")
    print("==================================================")

if __name__ == "__main__":
    main()
