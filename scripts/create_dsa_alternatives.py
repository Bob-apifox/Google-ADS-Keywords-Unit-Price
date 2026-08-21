import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers
import uuid

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

# 1. Create a Budget
budget_service = client.get_service("CampaignBudgetService")
budget_op = client.get_type("CampaignBudgetOperation")
budget = budget_op.create
budget.name = f"DSA-Alternatives-Budget-{uuid.uuid4().hex[:8]}"
budget.amount_micros = 20000000 # $20
budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
budget_response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[budget_op])
budget_resource_name = budget_response.results[0].resource_name

# 2. Create the Campaign
campaign_service = client.get_service("CampaignService")
campaign_op = client.get_type("CampaignOperation")
campaign = campaign_op.create
campaign.name = "Google-Sa-DSA-Alternatives-Global"
campaign.status = client.enums.CampaignStatusEnum.PAUSED # Pause first, enable after setup
campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
campaign.campaign_budget = budget_resource_name

# Fix Target CPA bidding for v15+
campaign.maximize_conversions.target_cpa_micros = 2500000 # $2.50
campaign.bidding_strategy_type = client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSIONS

# Fix Tracking Template
campaign.tracking_url_template = "{lpurl}?utm_source=google_dsa&utm_medium={network}&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={targetid}"

# Fix Network settings and EU political ads
campaign.network_settings.target_google_search = True
campaign.network_settings.target_search_network = True
campaign.network_settings.target_content_network = False
campaign.network_settings.target_partner_search_network = False
try:
    campaign.contains_eu_political_advertising = False
except Exception:
    pass # In case it's not a boolean attribute in this version

# Enable DSA setting
campaign.dynamic_search_ads_setting.domain_name = "apidog.com"
campaign.dynamic_search_ads_setting.language_code = "en"

campaign_response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=[campaign_op])
campaign_resource_name = campaign_response.results[0].resource_name
print(f"Created DSA Campaign: {campaign_resource_name}")

# 3. Create Ad Groups, Webpage Criteria, and Ads
ad_group_service = client.get_service("AdGroupService")
ad_group_criterion_service = client.get_service("AdGroupCriterionService")
ad_group_ad_service = client.get_service("AdGroupAdService")

competitors = [
    {"name": "Postman", "url": "https://apidog.com/blog/best-postman-alternative/", "desc": "Tired of Postman pricing? Switch to Apidog for free team collaboration."},
    {"name": "Insomnia", "url": "https://apidog.com/blog/best-insomnia-alternative/", "desc": "Looking for an Insomnia alternative? Import your data to Apidog in 1 click."},
    {"name": "SwaggerHub", "url": "https://apidog.com/blog/swaggerhub-alternative/", "desc": "Design APIs faster. Switch from SwaggerHub to Apidog for a modern experience."},
    {"name": "ReadMe", "url": "https://apidog.com/blog/readme-alternative/", "desc": "Better API documentation without the cost. The best ReadMe alternative."},
    {"name": "ReadyAPI", "url": "https://apidog.com/blog/readyapi-alternative/", "desc": "Heavy desktop tools slowing you down? Switch from ReadyAPI to Apidog."},
    {"name": "SoapUI", "url": "https://apidog.com/blog/soapui-alternative/", "desc": "Modernize your API testing. Move away from SoapUI to a faster platform."},
    {"name": "Mintlify", "url": "https://apidog.com/blog/mintlify-alternative/", "desc": "Auto-generate beautiful API docs. The ultimate Mintlify alternative."},
    {"name": "Bruno", "url": "https://apidog.com/blog/bruno-alternative/", "desc": "Need a powerful API client? Apidog is the perfect alternative to Bruno."},
    {"name": "Hoppscotch", "url": "https://apidog.com/blog/hoppscotch-alternative/", "desc": "Need better team management? Switch from Hoppscotch to Apidog today."}
]

for comp in competitors:
    # Ad Group
    ag_op = client.get_type("AdGroupOperation")
    ag = ag_op.create
    ag.campaign = campaign_resource_name
    ag.name = f"DSA-{comp['name']}-Alternative"
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag_resp = ad_group_service.mutate_ad_groups(customer_id=customer_id, operations=[ag_op])
    ag_resource_name = ag_resp.results[0].resource_name
    print(f"Created Ad Group: {ag_resource_name}")

    # Webpage Criterion (Exact URL)
    agc_op = client.get_type("AdGroupCriterionOperation")
    agc = agc_op.create
    agc.ad_group = ag_resource_name
    agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    webpage = agc.webpage
    webpage.criterion_name = f"URL Exact: {comp['url']}"
    
    # Use exact webpage condition
    condition = client.get_type("WebpageConditionInfo")
    condition.operand = client.enums.WebpageConditionOperandEnum.URL
    condition.operator = client.enums.WebpageConditionOperatorEnum.EQUALS
    condition.argument = comp['url']
    webpage.conditions.append(condition)
    
    ad_group_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=[agc_op])

    # Dynamic Search Ad
    ad_op = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_op.create
    ad_group_ad.ad_group = ag_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    
    ad = ad_group_ad.ad
    ad.dynamic_search_ad.description1 = comp['desc']
    ad.dynamic_search_ad.description2 = "Sign up for free and start testing APIs instantly. Import in seconds."
    
    ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])

# Pause Old DSA Postman
query = "SELECT campaign.id, campaign.resource_name FROM campaign WHERE campaign.name = 'Google-Sa-DSA-Postman-Global'"
response = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
for row in response:
    pause_op = client.get_type("CampaignOperation")
    pause_op.update.resource_name = row.campaign.resource_name
    pause_op.update.status = client.enums.CampaignStatusEnum.PAUSED
    client.copy_from(pause_op.update_mask, protobuf_helpers.field_mask(None, pause_op.update._pb))
    campaign_service.mutate_campaigns(customer_id=customer_id, operations=[pause_op])
    print("Paused old Google-Sa-DSA-Postman-Global")

# Enable New Campaign
enable_op = client.get_type("CampaignOperation")
enable_op.update.resource_name = campaign_resource_name
enable_op.update.status = client.enums.CampaignStatusEnum.ENABLED
client.copy_from(enable_op.update_mask, protobuf_helpers.field_mask(None, enable_op.update._pb))
campaign_service.mutate_campaigns(customer_id=customer_id, operations=[enable_op])
print("Enabled new Google-Sa-DSA-Alternatives-Global")
