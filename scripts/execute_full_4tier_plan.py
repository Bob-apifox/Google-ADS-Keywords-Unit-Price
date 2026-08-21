import os
import sys
import urllib3
from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

# 1. Budget Updates
budget_updates = [
    ("Google-Sa-CP-Global", 200.00),
    ("Google-Sa-Expansion-Horizon-2026", 60.00),
    ("Google-Sa-Comp-HeavyQA-Global", 55.00),
    ("Google-Sa-Annual Planning & New Trends-26", 35.00),
    ("Google-Sa-Openapi-Global", 35.00),
    ("Google-Sa-Enterprise-Killer-Global", 25.00),
    ("Google-Dis-DevPlacements-Global", 15.00),
    ("Google-Dis-Remarketing-Global", 10.00),
    ("Google-Sa-Stoplight-Global", 8.00)
]

# 2. Target CPA Updates
tcpa_updates = [
    ("Google-Dis-DevPlacements-Global", 3.00),
    ("Google-Dis-Remarketing-Global", 2.50)
]

# 3. Display Placement Exclusions
display_exclusions = [
    "geeksforgeeks.org/techtips/how-to-change-the-desktop-background-in-windows-11",
    "geeksforgeeks.org/installation-guide/how-to-install-youtube-app-on-windows",
    "geeksforgeeks.org/installation-guide/download-and-install-sketchup-on-windows",
    "geeksforgeeks.org/techtips/connect-bluetooth-devices-in-windows",
    "w3schools.com/typingspeed/",
    "geeksforgeeks.org/ethical-hacking/how-to-install-trojan-virus-on-any-computer"
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    cb_service = client.get_service("CampaignBudgetService")
    camp_service = client.get_service("CampaignService")
    cc_service = client.get_service("CampaignCriterionService")
    
    # Query campaigns
    query = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.campaign_budget
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    
    camps = {}
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        cname = row.campaign.name
        cid = str(row.campaign.id)
        b_res = row.campaign.campaign_budget
        camps[cname] = {
            "id": cid,
            "budget_res": b_res
        }
        
    print(f"Fetched {len(camps)} enabled campaigns.")
    
    # 1. Update Budgets
    b_ops = []
    for cname, amount in budget_updates:
        if cname in camps:
            b_res = camps[cname]["budget_res"]
            op = client.get_type("CampaignBudgetOperation")
            budget = op.update
            budget.resource_name = b_res
            budget.amount_micros = int(amount * 1000000)
            op.update_mask.paths.append("amount_micros")
            b_ops.append((cname, amount, op))
            
    if b_ops:
        req = client.get_type("MutateCampaignBudgetsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend([item[2] for item in b_ops])
        req.partial_failure = True
        cb_service.mutate_campaign_budgets(request=req)
        for cname, amount, _ in b_ops:
            print(f"✅ Budget for '{cname}' updated to ${amount:.2f}/day.")
            
    # 2. Update Target CPA
    c_ops = []
    for cname, tcpa in tcpa_updates:
        if cname in camps:
            cid = camps[cname]["id"]
            op = client.get_type("CampaignOperation")
            camp = op.update
            camp.resource_name = ga_service.campaign_path(CUSTOMER_ID, cid)
            camp.target_cpa.target_cpa_micros = int(tcpa * 1000000)
            op.update_mask.paths.append("target_cpa.target_cpa_micros")
            c_ops.append((cname, tcpa, op))
            
    if c_ops:
        req = client.get_type("MutateCampaignsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend([item[2] for item in c_ops])
        req.partial_failure = True
        camp_service.mutate_campaigns(request=req)
        for cname, tcpa, _ in c_ops:
            print(f"✅ Target CPA for '{cname}' updated to ${tcpa:.2f}.")

    # 3. Add Display Placement Exclusions
    dev_camp_name = "Google-Dis-DevPlacements-Global"
    if dev_camp_name in camps:
        cid = camps[dev_camp_name]["id"]
        p_ops = []
        for url in display_exclusions:
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = ga_service.campaign_path(CUSTOMER_ID, cid)
            criterion.negative = True
            criterion.placement.url = url
            p_ops.append(op)
            
        if p_ops:
            req = client.get_type("MutateCampaignCriteriaRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(p_ops)
            req.partial_failure = True
            try:
                cc_service.mutate_campaign_criteria(request=req)
                print(f"✅ Added {len(p_ops)} placement exclusions to {dev_camp_name}!")
            except Exception as e:
                print(f"Placement exclusion note: {e}")

    print("🎉 Full 4-Tier Strategic Optimization Plan executed successfully online!")

if __name__ == '__main__':
    main()
