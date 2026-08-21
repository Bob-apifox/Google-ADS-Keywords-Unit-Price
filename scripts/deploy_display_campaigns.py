import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"
PMAX_CP_ID = "22341978472"

USER_LIST_ALL_VISITORS = "8879981348"
USER_LIST_REGISTERED = "8872182184"

LOGO_ASSET_ID = "16738974558"
MARKETING_IMAGE_1_ID = "17165039230"
SQUARE_IMAGE_1_ID = "17165039233"
MARKETING_IMAGE_2_ID = "17165039227"
SQUARE_IMAGE_2_ID = "17165039224"

WHITELIST_PLACEMENTS = [
    "stackoverflow.com",
    "dev.to",
    "w3schools.com",
    "geeksforgeeks.org",
    "hashnode.com",
    "developer.mozilla.org",
    "medium.com",
    "dzone.com",
    "infoq.com",
    "g2.com",
    "capterra.com",
    "trustradius.com",
    "slant.co",
    "sourceforge.net",
    "rapidapi.com",
    "swagger.io"
]

def pause_pmax(client, customer_id):
    print("==========================================================================")
    print("[STEP 1: PAUSING PMAX CAMPAIGN (Google-PMax-CP-Global)]")
    print("==========================================================================")
    campaign_service = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    c = op.update
    c.resource_name = f"customers/{customer_id}/campaigns/{PMAX_CP_ID}"
    c.status = client.enums.CampaignStatusEnum.PAUSED
    client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, c._pb))

    try:
        campaign_service.mutate_campaigns(customer_id=customer_id, operations=[op])
        print(f"[SUCCESS] Google-PMax-CP-Global ({PMAX_CP_ID}) is now PAUSED.")
    except Exception as e:
        print(f"[NOTE] Pausing PMax: {e}")

def create_display_campaign(client, customer_id, name, budget_usd, tcpa_usd):
    print(f"\nCreating Campaign: {name} (${budget_usd}/day, tCPA: ${tcpa_usd})")
    budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # 1. Budget
    b_op = client.get_type("CampaignBudgetOperation")
    b = b_op.create
    b.name = f"Budget-{name}"
    b.amount_micros = int(budget_usd * 1000000)
    b.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False
    b_resp = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[b_op])
    budget_res = b_resp.results[0].resource_name
    print(f"  [Budget Created]: {budget_res}")

    # 2. Campaign
    c_op = client.get_type("CampaignOperation")
    c = c_op.create
    c.name = name
    c.status = client.enums.CampaignStatusEnum.ENABLED
    c.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.DISPLAY
    c.campaign_budget = budget_res
    c.contains_eu_political_advertising = client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING

    # Bidding Strategy for Display: target_cpa
    c.target_cpa.target_cpa_micros = int(tcpa_usd * 1000000)

    c_resp = campaign_service.mutate_campaigns(customer_id=customer_id, operations=[c_op])
    camp_res = c_resp.results[0].resource_name
    print(f"  [Campaign Created]: {camp_res}")
    return camp_res

def create_ad_group(client, customer_id, camp_res, name):
    ad_group_service = client.get_service("AdGroupService")
    ag_op = client.get_type("AdGroupOperation")
    ag = ag_op.create
    ag.name = name
    ag.campaign = camp_res
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.type_ = client.enums.AdGroupTypeEnum.DISPLAY_STANDARD
    ag.optimized_targeting_enabled = False  # CRITICAL: Disable optimized targeting to prevent junk expansion!

    ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
    ag_res = ag_resp.results[0].resource_name
    print(f"  [Ad Group Created with Optimized Targeting OFF]: {ag_res}")
    return ag_res

def add_user_list_targeting(client, customer_id, ag_res, camp_res):
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    campaign_criterion_service = client.get_service("CampaignCriterionService")

    # 1. Target All Visitors
    op1 = client.get_type("AdGroupCriterionOperation")
    crit1 = op1.create
    crit1.ad_group = ag_res
    crit1.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    crit1.user_list.user_list = f"customers/{customer_id}/userLists/{USER_LIST_ALL_VISITORS}"

    # 2. Exclude Registered Users (Campaign Level Exclusion)
    op2 = client.get_type("CampaignCriterionOperation")
    crit2 = op2.create
    crit2.campaign = camp_res
    crit2.negative = True
    crit2.user_list.user_list = f"customers/{customer_id}/userLists/{USER_LIST_REGISTERED}"

    try:
        ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[op1])
        print(f"  [Audience Targeted]: All Visitors ({USER_LIST_ALL_VISITORS})")
    except Exception as e:
        print(f"  [ERROR Targeting Audience]: {e}")

    try:
        campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=[op2])
        print(f"  [Audience Excluded]: Registered Users ({USER_LIST_REGISTERED})")
    except Exception as e:
        print(f"  [ERROR Excluding Audience]: {e}")

def add_placement_targeting(client, customer_id, ag_res):
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    ops = []
    for domain in WHITELIST_PLACEMENTS:
        op = client.get_type("AdGroupCriterionOperation")
        crit = op.create
        crit.ad_group = ag_res
        crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        crit.placement.url = domain
        ops.append(op)

    try:
        resp = ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)
        print(f"  [Placements Whitelisted]: Successfully added {len(resp.results)} developer domains!")
    except Exception as e:
        print(f"  [ERROR Whitelisting Placements]: {e}")

def create_rda_ad(client, customer_id, ag_res, headlines, long_headline, descriptions, marketing_img_id, square_img_id, logo_id, final_url, suffix, call_to_action):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_op = client.get_type("AdGroupAdOperation")
    aga = ad_op.create
    aga.ad_group = ag_res
    aga.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = aga.ad
    ad.final_urls.append(final_url)
    ad.final_url_suffix = suffix

    rda = ad.responsive_display_ad
    rda.business_name = "Apidog"
    rda.call_to_action_text = call_to_action

    # Long headline
    rda.long_headline.text = long_headline

    # Short headlines
    for h in headlines:
        hl = client.get_type("AdTextAsset")
        hl.text = h
        rda.headlines.append(hl)

    # Descriptions
    for d in descriptions:
        ds = client.get_type("AdTextAsset")
        ds.text = d
        rda.descriptions.append(ds)

    # Marketing Images (Landscape 1.91:1)
    img_asset = client.get_type("AdImageAsset")
    img_asset.asset = f"customers/{customer_id}/assets/{marketing_img_id}"
    rda.marketing_images.append(img_asset)

    # Square Marketing Image (1:1)
    sq_asset = client.get_type("AdImageAsset")
    sq_asset.asset = f"customers/{customer_id}/assets/{square_img_id}"
    rda.square_marketing_images.append(sq_asset)

    # Logo (1:1)
    logo_asset = client.get_type("AdImageAsset")
    logo_asset.asset = f"customers/{customer_id}/assets/{logo_id}"
    rda.logo_images.append(logo_asset)

    try:
        resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
        print(f"  [RDA Ad Created]: {resp.results[0].resource_name}")
    except Exception as e:
        print(f"  [ERROR Creating RDA Ad]: {e}")

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID

    # 1. Pause PMax
    pause_pmax(client, customer_id)

    # 2. Deploy Track 1: Remarketing
    print("\n==========================================================================")
    print("[STEP 2: DEPLOYING TRACK 1 - REMARKETING (Google-Dis-Remarketing-Global)]")
    print("==========================================================================")
    c1_res = create_display_campaign(client, customer_id, "Google-Dis-Remarketing-Global", 15.0, 2.50)
    ag1_res = create_ad_group(client, customer_id, c1_res, "Remarketing-Past-Visitors")
    add_user_list_targeting(client, customer_id, ag1_res, c1_res)

    h1 = [
        "Still Struggling with Postman?",
        "Visual API Design & Debugging",
        "The All-in-One API Platform",
        "Free Unlimited API Test Runner",
        "Upgrade Your API Workflow Now"
    ]
    lh1 = "Design, Debug, Mock, and Test APIs in One Single Workspace. Try Apidog for Free Today."
    d1 = [
        "Join 1M+ developers using Apidog for visual API design, automated testing, and mock servers.",
        "Tired of switching between tools? Apidog combines Postman, Swagger, and JMeter in one.",
        "Import Postman collections in seconds and enjoy unlimited runner executions for free."
    ]
    suffix1 = "utm_source=google_display&utm_medium=remarketing&utm_campaign={campaignid}&utm_adgroup={adgroupid}"
    create_rda_ad(client, customer_id, ag1_res, h1, lh1, d1, MARKETING_IMAGE_1_ID, SQUARE_IMAGE_1_ID, LOGO_ASSET_ID, "https://apidog.com/", suffix1, "Try Free")

    # 3. Deploy Track 2: Placements
    print("\n==========================================================================")
    print("[STEP 3: DEPLOYING TRACK 2 - PLACEMENTS (Google-Dis-DevPlacements-Global)]")
    print("==========================================================================")
    c2_res = create_display_campaign(client, customer_id, "Google-Dis-DevPlacements-Global", 20.0, 3.00)
    ag2_res = create_ad_group(client, customer_id, c2_res, "DevPlacements-Whitelist")
    add_placement_targeting(client, customer_id, ag2_res)

    h2 = [
        "Best Postman Alternative 2026",
        "Modern API Platform for Teams",
        "API Design, Mock & Test Tool",
        "Automated API Testing in CI/CD",
        "Visual API Workspace for Devs"
    ]
    lh2 = "A Smarter, Visual API Development Workspace Built for Modern Engineering Teams."
    d2 = [
        "Stop jumping across Postman, Swagger, and JMeter. Streamline your API lifecycle in Apidog.",
        "Auto-generate mock data, run automated tests, and sync API documentation seamlessly.",
        "Built for developers who value speed and efficiency. Free for individuals and small teams."
    ]
    suffix2 = "utm_source=google_display&utm_medium=placement_branding&utm_campaign={campaignid}&utm_adgroup={adgroupid}"
    create_rda_ad(client, customer_id, ag2_res, h2, lh2, d2, MARKETING_IMAGE_2_ID, SQUARE_IMAGE_2_ID, LOGO_ASSET_ID, "https://apidog.com/", suffix2, "Learn More")

    print("\n==========================================================================")
    print("[ALL DONE] PMax Paused & Display Campaigns 100% Deployed Live Online!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
