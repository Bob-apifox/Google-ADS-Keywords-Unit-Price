import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
TRACKING_SUFFIX = "utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

def execute():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ag_service = client.get_service('AdGroupService')
    agc_service = client.get_service('AdGroupCriterionService')
    ad_service = client.get_service('AdGroupAdService')

    camp_names = [
        'Google-Sa-Solutions-AI-LLM-Global',
        'Google-Sa-Debug-Global',
        'Google-Sa-CP-AR'
    ]
    
    camp_res_map = {}
    camps_sql = ", ".join([f"'{c}'" for c in camp_names])
    q_camp = f"SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name IN ({camps_sql})"
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            camp_res_map[row.campaign.name] = row.campaign.resource_name
            print(f"Found campaign: {row.campaign.name}")

    ag_data = []
    
    if 'Google-Sa-Solutions-AI-LLM-Global' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-Solutions-AI-LLM-Global',
            'name': 'AI-Coding-Tools',
            'kws': ["ai coding assistant", "ai code generator for api", "cursor ai alternative"],
            'url': 'https://apidog.com/',
            'headlines': ["AI Code Generator for API", "Cursor AI Alternative", "Automate API Code", "Smart AI API Tool", "Code APIs with AI"],
            'descriptions': ["Instantly generate API code and mock data using advanced AI.", "The perfect alternative to Cursor for API development and testing."]
        })
        
    if 'Google-Sa-Debug-Global' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-Debug-Global',
            'name': 'Debug-React-DevTools',
            'kws': ["react devtools alternative", "network tab debugger", "debug api payload"],
            'url': 'https://apidog.com/api-debug/',
            'headlines': ["React DevTools Alternative", "Debug API Payloads", "Network Tab Debugger", "Visual API Debugging", "Better API DevTools"],
            'descriptions': ["Stop guessing what went wrong. Visually debug API payloads seamlessly.", "A powerful alternative to standard React DevTools and network tabs."]
        })
        ag_data.append({
            'campaign': 'Google-Sa-Debug-Global',
            'name': 'Debug-Frontend-Dart',
            'kws': ["flutter api debugging", "dart api client"],
            'url': 'https://apidog.com/api-debug/',
            'headlines': ["Flutter API Debugging", "Dart API Client", "Test APIs in Flutter", "Mobile API Debugging", "Advanced Dart Client"],
            'descriptions': ["The ultimate API client for Flutter and Dart developers.", "Debug mobile app API requests instantly with a powerful interface."]
        })

    if 'Google-Sa-CP-AR' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-CP-AR',
            'name': 'AR-Native-API-Testing',
            'kws': ["بديل postman", "اختبار واجهة برمجة التطبيقات"],
            'url': 'https://apidog.com/',
            'headlines': ["Best Postman Alternative", "Advanced API Testing", "Free API Tool", "Better API Workflows", "Try Apidog for Free"],
            'descriptions': ["Switch from Postman today. Unlimited API testing without runner limits.", "A complete API platform for your entire development team."]
        })

    if not ag_data:
        print("No campaigns found to execute.")
        return

    # 1. Create Ad Groups (already created)
    # 2. Create Keywords (already created)

    # 3. Create RSAs
    rsa_ops = []
    generics = ["All-in-One API Workspace", "Complete API Platform", "Visual API Editor", "Automated API Testing", "Better API Documentation", "Try Apidog for Free", "Seamless API Collaboration", "Elevate API Workflows", "API Design Made Easy", "Smart API Mocking"]
    
    for g in ag_data:
        # Fetch the AdGroup Resource Name since we didn't save it in this run
        ag_res = None
        q_ag = f"SELECT ad_group.resource_name FROM ad_group WHERE ad_group.name = '{g['name']}' AND campaign.id = {camp_res_map[g['campaign']].split('/')[-1]}"
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
            for row in batch.results:
                ag_res = row.ad_group.resource_name
                break
        
        if not ag_res:
            print(f"AdGroup not found for {g['name']}")
            continue

        op = client.get_type("AdGroupAdOperation")
        ad_group_ad = op.create
        ad_group_ad.ad_group = ag_res
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        ad_group_ad.ad.final_urls.append(g['url'])
        ad_group_ad.ad.tracking_url_template = f"{{lpurl}}?{TRACKING_SUFFIX}"
        
        final_headlines = []
        for h in (g['headlines'] + generics):
            if h not in final_headlines:
                final_headlines.append(h)
        final_headlines = final_headlines[:15]
        
        for h in final_headlines:
            asset = client.get_type("AdTextAsset")
            asset.text = h[:30]
            ad_group_ad.ad.responsive_search_ad.headlines.append(asset)
            
        final_desc = (g['descriptions'] + ["An integrated platform for API design, debugging, testing, and documentation.", "Empower your frontend and backend teams to collaborate flawlessly on APIs."])[:4]
        for d in final_desc:
            asset = client.get_type("AdTextAsset")
            asset.text = d[:90]
            ad_group_ad.ad.responsive_search_ad.descriptions.append(asset)
            
        rsa_ops.append(op)
        
    if rsa_ops:
        rsa_resp = ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=rsa_ops)
        print(f"Created {len(rsa_resp.results)} RSAs.")
        
    print("Expansion Track 1 & 2 Execution Complete!")

if __name__ == '__main__':
    execute()
