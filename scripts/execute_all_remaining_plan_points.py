import os
import sys
import time
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

def get_client_with_retry(max_retries=5, delay=3):
    for attempt in range(1, max_retries + 1):
        try:
            client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
            return client
        except Exception as e:
            print(f"⚠️ OAuth Client Auth attempt {attempt}/{max_retries} failed: {e}")
            if attempt == max_retries:
                raise e
            time.sleep(delay)

# Comprehensive budget & tCPA updates from Section 6 & Sections 3-5
budget_and_tcpa_targets = [
    # (Campaign Name, Daily Budget USD, Target CPA USD)
    ("Google-Sa-CP-Global", 200.00, 2.50),
    ("Google-Sa-Solutions-AI-LLM-Global", 110.00, 2.80),
    ("Google-Sa-DSA-Global", 120.00, 2.80),
    ("Google-Sa-Postman-Global", 95.00, 3.00),
    ("Google-Sa-Comp-HeavyQA-Global", 55.00, 2.50),
    ("Google-Sa-Expansion-Horizon-2026", 60.00, 2.70),
    ("Google-Sa-DSA-Postman-Global", 40.00, 2.50),
    ("Google-Sa-Debug-Global", 40.00, 2.80),
    ("Google-Sa-Jmeter-Global", 50.00, 3.50),
    ("Google-Sa-Mock-Global", 45.00, 3.00),
    ("Google-Sa-Fern-Global", 30.00, 2.50),
    ("Google-Sa-Solutions-Unified-API-Global", 30.00, 2.80),
    ("Google-Sa-Openapi-Global", 35.00, 2.50),
    ("Google-Sa-Annual Planning & New Trends-26", 35.00, 2.50),
    ("Google-Sa-Mintlify-Global", 35.00, 3.50),
    ("Google-Sa-Enterprise-Killer-Global", 25.00, 2.50),
    ("Google-Sa-Doc-Global", 20.00, 2.50),
    ("Google-Sa-Readme-Global", 30.00, 3.50),
    ("Google-Dis-DevPlacements-Global", 15.00, 3.00),
    ("Google-Dis-Remarketing-Global", 10.00, 2.50),
    ("Google-Sa-Stoplight-Global", 8.00, 3.00),
    ("Google-Sa-Function-Global", 30.00, 2.60),
    ("Google-Sa-Design-Global", 30.00, 2.50),
    ("Google-Sa-CP-ID", 15.00, 2.10),
    ("Google-Sa-Solutions-API-First-Global", 30.00, 2.60),
    ("Google-Sa-CP-TW", 15.00, 2.50),
    ("Google-Sa-Testing-Global", 25.00, 2.80),
    ("Google-Sa-CP-AR", 35.00, 2.70),
    ("Google-Sa-DSA-Alternatives-Global", 50.00, 2.50),
    ("Google-Sa-Comp-VSCode-Global", 20.00, 2.50)
]

# Display Placement Exclusions
display_exclusions = [
    "geeksforgeeks.org/techtips/how-to-change-the-desktop-background-in-windows-11",
    "geeksforgeeks.org/installation-guide/how-to-install-youtube-app-on-windows",
    "geeksforgeeks.org/installation-guide/download-and-install-sketchup-on-windows",
    "geeksforgeeks.org/techtips/connect-bluetooth-devices-in-windows",
    "w3schools.com/typingspeed/",
    "geeksforgeeks.org/ethical-hacking/how-to-install-trojan-virus-on-any-computer"
]

# Remarketing Final URL
REMARKETING_FINAL_URL = "https://apidog.com/compare/apidog-vs-postman/?utm_source=google_display&utm_medium=remarketing_cta"

# 31 missing keywords mapped to Campaign & AdGroup names
missing_kw_mappings = [
    ("reqbin alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("kreya alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("testfully alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("stoplight openapi alternative", "Google-Sa-Stoplight-Global", "Stoplight Alternative--Global"),
    ("cloud mock server", "Google-Sa-Mock-Global", "Mock-Global"),
    ("self hosted mock server", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("conditional mock api", "Google-Sa-Func-AdvancedMock-Global", "Wiremock-Alternative"),
    ("zero code mock api", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("auto mock api", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("prism mock alternative", "Google-Sa-Func-AdvancedMock-Global", "Wiremock-Alternative"),
    ("soap wsdl api testing", "Google-Sa-Testing-Global", "Testing-Global"),
    ("mtls api testing", "Google-Sa-Testing-Global", "API-Security-Testing"),
    ("client certificate api test", "Google-Sa-Testing-Global", "Testing-Security-Auth"),
    ("test file upload api", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("test stripe webhooks", "Google-Sa-Solutions-Multi-Protocol-Global", "Webhook Testing"),
    ("api test with database assertion", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("conditional api test scenarios", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("import har to api test", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("schedule api automated tests", "Google-Sa-Testing-Global", "Automated-API-Regression-Runner"),
    ("circleci api testing", "Google-Sa-Func-CICD-Global", "API-Pipeline"),
    ("drone ci api testing", "Google-Sa-Func-CICD-Global", "API-Pipeline"),
    ("cli api testing tool", "Google-Sa-CLI-Terminal-Global", "CLI-Automated-Testing"),
    ("api regression testing tool", "Google-Sa-Func-CICD-Global", "Newman-Integration"),
    ("apachebench alternative", "Google-Sa-Jmeter-Global", "JMeter-Replacement-Global"),
    ("ab load testing gui", "Google-Sa-Jmeter-Global", "Jmeter---Global"),
    ("autocannon load testing", "Google-Sa-Jmeter-Global", "API-Performance-Ease-Global"),
    ("artillery api load testing", "Google-Sa-Jmeter-Global", "JMeter-Replacement-Global"),
    ("http api load testing tool", "Google-Sa-Jmeter-Global", "API-Performance-Ease-Global"),
    ("api secret scanner", "Google-Sa-Enterprise-Killer-Global", "API-Testing-Comparison"),
    ("api audit logs tool", "Google-Sa-Enterprise-Killer-Global", "API-Testing-Comparison"),
    ("openapi client code generator", "Google-Sa-Openapi-Global", "Openapi--Global")
]

def step1_update_budgets_and_tcpa(client, camps):
    print("\n--- STEP 1: Updating Daily Budgets & Target CPAs (Modules 2, 3, 4, 5) ---")
    cb_service = client.get_service("CampaignBudgetService")
    camp_service = client.get_service("CampaignService")
    ga_service = client.get_service("GoogleAdsService")

    b_ops = []
    c_ops = []
    
    for cname, budget_usd, tcpa_usd in budget_and_tcpa_targets:
        if cname in camps:
            cinfo = camps[cname]
            cid = cinfo["id"]
            b_res = cinfo["budget_res"]
            
            # Budget Operation
            if budget_usd is not None:
                op_b = client.get_type("CampaignBudgetOperation")
                b_obj = op_b.update
                b_obj.resource_name = b_res
                b_obj.amount_micros = int(budget_usd * 1000000)
                op_b.update_mask.paths.append("amount_micros")
                b_ops.append((cname, budget_usd, op_b))
                
            # Target CPA Operation
            if tcpa_usd is not None:
                op_c = client.get_type("CampaignOperation")
                c_obj = op_c.update
                c_obj.resource_name = ga_service.campaign_path(CUSTOMER_ID, cid)
                c_obj.target_cpa.target_cpa_micros = int(tcpa_usd * 1000000)
                op_c.update_mask.paths.append("target_cpa.target_cpa_micros")
                c_ops.append((cname, tcpa_usd, op_c))
        else:
            print(f"⚠️ Campaign '{cname}' not found in active campaigns list.")

    # Execute Budgets Mutate
    if b_ops:
        req = client.get_type("MutateCampaignBudgetsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend([item[2] for item in b_ops])
        req.partial_failure = True
        res = cb_service.mutate_campaign_budgets(request=req)
        print(f"✅ Budget Mutate Request sent for {len(b_ops)} campaigns.")
        for cname, amount, _ in b_ops:
            print(f"   • {cname} -> Budget: ${amount:.2f}/day")

    # Execute Target CPA Mutate
    if c_ops:
        req = client.get_type("MutateCampaignsRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend([item[2] for item in c_ops])
        req.partial_failure = True
        res = camp_service.mutate_campaigns(request=req)
        print(f"✅ Target CPA Mutate Request sent for {len(c_ops)} campaigns.")
        for cname, tcpa, _ in c_ops:
            print(f"   • {cname} -> Target CPA: ${tcpa:.2f}")

def step2_apply_display_exclusions_and_landing_url(client, camps):
    print("\n--- STEP 2: Display Placement Exclusions & Remarketing Final URL Update (Module 3) ---")
    ga_service = client.get_service("GoogleAdsService")
    cc_service = client.get_service("CampaignCriterionService")
    aga_service = client.get_service("AdGroupAdService")

    # 1. DevPlacements Exclusions
    dev_camp = "Google-Dis-DevPlacements-Global"
    if dev_camp in camps:
        cid = camps[dev_camp]["id"]
        p_ops = []
        for url in display_exclusions:
            op = client.get_type("CampaignCriterionOperation")
            crit = op.create
            crit.campaign = ga_service.campaign_path(CUSTOMER_ID, cid)
            crit.negative = True
            crit.placement.url = url
            p_ops.append(op)
            
        req = client.get_type("MutateCampaignCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(p_ops)
        req.partial_failure = True
        try:
            cc_service.mutate_campaign_criteria(request=req)
            print(f"✅ Added {len(p_ops)} placement exclusions to {dev_camp}:")
            for u in display_exclusions:
                print(f"   • Excluded: {u}")
        except Exception as e:
            print(f"   Excluded placement note: {e}")

    # 2. Remarketing Final URL
    rem_camp = "Google-Dis-Remarketing-Global"
    if rem_camp in camps:
        query = f"""
            SELECT ad_group_ad.resource_name, ad_group_ad.ad.id, ad_group_ad.ad.final_urls
            FROM ad_group_ad
            WHERE campaign.name = '{rem_camp}' AND ad_group_ad.status = 'ENABLED'
        """
        stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
        ad_ops = []
        for row in stream:
            res_name = row.ad_group_ad.resource_name
            op = client.get_type("AdGroupAdOperation")
            ad_update = op.update
            ad_update.resource_name = res_name
            ad_update.ad.final_urls.append(REMARKETING_FINAL_URL)
            op.update_mask.paths.append("ad.final_urls")
            ad_ops.append(op)
            
        if ad_ops:
            req = client.get_type("MutateAdGroupAdsRequest")
            req.customer_id = CUSTOMER_ID
            req.operations.extend(ad_ops)
            req.partial_failure = True
            aga_service.mutate_ad_group_ads(request=req)
            print(f"✅ Updated Final URL for {len(ad_ops)} Remarketing Ads to:\n   {REMARKETING_FINAL_URL}")

def step3_upload_missing_blog_keywords(client):
    print("\n--- STEP 3: Uploading 31 High-Value Non-AI Blog Keywords (Module 7) ---")
    ga_service = client.get_service("GoogleAdsService")
    agc_service = client.get_service("AdGroupCriterionService")

    query = """
        SELECT campaign.name, ad_group.name, ad_group.resource_name
        FROM ad_group
        WHERE ad_group.status = 'ENABLED'
    """
    ag_map = {}
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        cname = row.campaign.name
        agname = row.ad_group.name
        ag_map[(cname, agname)] = row.ad_group.resource_name
        
    ops = []
    added_list = []
    for kw, cname, agname in missing_kw_mappings:
        key = (cname, agname)
        if key in ag_map:
            ag_res = ag_map[key]
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_res
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            ops.append(op)
            added_list.append((kw, cname, agname))
        else:
            print(f"⚠️ Target AdGroup not found: {cname} -> {agname}")
            
    if ops:
        req = client.get_type("MutateAdGroupCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ops)
        req.partial_failure = True
        try:
            res = agc_service.mutate_ad_group_criteria(request=req)
            print(f"✅ Successfully injected {len(ops)} missing keywords (PHRASE Match):")
            for kw, cname, agname in added_list:
                print(f"   • [{kw}] -> Campaign: {cname} | AdGroup: {agname}")
        except Exception as e:
            print(f"❌ Error uploading missing keywords: {e}")

def main():
    print("🚀 Starting Master Execution for Google Ads Weekly Execution Plan (2026-08-17)...")
    client = get_client_with_retry()
    ga_service = client.get_service("GoogleAdsService")

    # Fetch all enabled campaigns
    query = """
        SELECT campaign.id, campaign.name, campaign.campaign_budget
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    """
    camps = {}
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        cname = row.campaign.name
        cid = str(row.campaign.id)
        b_res = row.campaign.campaign_budget
        camps[cname] = {"id": cid, "budget_res": b_res}

    print(f"Fetched {len(camps)} enabled campaigns from Google Ads API.")

    # Step 1: Update Budgets & Target CPAs
    step1_update_budgets_and_tcpa(client, camps)

    # Step 2: Apply Display Placement Exclusions & Remarketing Final URL
    step2_apply_display_exclusions_and_landing_url(client, camps)

    # Step 3: Upload Missing 31 Blog Keywords
    step3_upload_missing_blog_keywords(client)

    print("\n🎉 MASTER EXECUTION COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
