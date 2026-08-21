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
    camp_service = client.get_service('CampaignService')
    cc_service = client.get_service('CampaignCriterionService')
    ag_service = client.get_service('AdGroupService')
    agc_service = client.get_service('AdGroupCriterionService')
    ad_service = client.get_service('AdGroupAdService')

    print(">>> Starting Execution Plan...")

    # 1. Fetch campaigns mapping
    camp_names = [
        'Google-Sa-CP-DE',
        'Google-Sa-Testing-Global',
        'Google-Sa-Doc-Global',
        'Google-Sa-Insomnia-Global',
        'Google-Sa-Bruno-Global',
        'Google-Sa-Solutions-AI-LLM-Global',
        'Google-Sa-RapidAPI-Global',
        'Google-Sa-CP-ID'
    ]
    
    camp_res_map = {}
    camps_sql = ", ".join([f"'{c}'" for c in camp_names])
    q_camp = f"SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name IN ({camps_sql})"
    
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
        for row in batch.results:
            camp_res_map[row.campaign.name] = row.campaign.resource_name
            print(f"Found campaign: {row.campaign.name}")

    # ==========================================
    # 2. PAUSE CAMPAIGN
    # ==========================================
    if 'Google-Sa-CP-DE' in camp_res_map:
        camp_op = client.get_type("CampaignOperation")
        camp = camp_op.update
        camp.resource_name = camp_res_map['Google-Sa-CP-DE']
        camp.status = client.enums.CampaignStatusEnum.PAUSED
        camp_op.update_mask.paths.append("status")
        try:
            camp_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op])
            print("Paused Google-Sa-CP-DE")
        except GoogleAdsException as ex:
            print(f"Failed to pause DE: {ex}")

    # ==========================================
    # 3. ADD NEGATIVE KEYWORDS
    # ==========================================
    negatives_map = {
        'Google-Sa-Testing-Global': ['owasp juice shop', 'owasp zap desktop', 'owasp zap tool', 'nodezero', 'hackerai co', 'api enumeration tools'],
        'Google-Sa-Doc-Global': ['flask api', 'fastreport designer', 'software', 'api generate'],
        'Google-Sa-Insomnia-Global': ['mobile app development', 'pwa', 'progressive web app', 'vercel app', 'openhands'],
        'Google-Sa-Bruno-Global': ['app building software', 'conholdate', 'бесплатный api ключ deepseek', 'gemini web 2 api', 'bing web search api']
    }
    
    cc_ops = []
    for c_name, words in negatives_map.items():
        if c_name in camp_res_map:
            for w in words:
                op = client.get_type("CampaignCriterionOperation")
                crit = op.create
                crit.campaign = camp_res_map[c_name]
                crit.negative = True
                crit.keyword.text = w
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                cc_ops.append(op)
                
    if cc_ops:
        try:
            cc_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=cc_ops)
            print(f"Added {len(cc_ops)} negative keywords.")
        except GoogleAdsException as ex:
            print(f"Failed to add negatives: {ex}")

    # ==========================================
    # 4. CREATE NEW AD GROUPS & KWS & RSAS
    # ==========================================
    ag_data = []
    if 'Google-Sa-Solutions-AI-LLM-Global' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-Solutions-AI-LLM-Global',
            'name': 'AI-Schema-Designer',
            'kws': ["ai schema", "ai api designer", "generate api schema ai"],
            'url': 'https://apidog.com/',
            'headlines': ["Design APIs with AI", "Instantly Generate API Schema", "Smart API Designer", "AI API Schema Generator", "Automate API Design"],
            'descriptions': ["Design your APIs effortlessly using advanced AI schema generation.", "Stop designing manually. Let AI build your API schemas instantly."]
        })
        ag_data.append({
            'campaign': 'Google-Sa-Solutions-AI-LLM-Global',
            'name': 'AI-Boilerplate-Generator',
            'kws': ["ai boilerplate generator", "ai backend generator", "ai code generator for api"],
            'url': 'https://apidog.com/',
            'headlines': ["AI Boilerplate Generator", "AI Backend Code Generator", "Generate API Code with AI", "Smart Code Generation", "AI Driven API Workflow"],
            'descriptions': ["Instantly generate boilerplate code and backends for your APIs using AI.", "Speed up development. Get production-ready API code in seconds."]
        })
        
    if 'Google-Sa-RapidAPI-Global' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-RapidAPI-Global',
            'name': 'RapidAPI-Enterprise-Alternatives',
            'kws': ["rapidapi enterprise alternative", "rapidapi hub alternative", "migrate from rapidapi"],
            'url': 'https://apidog.com/',
            'headlines': ["Best RapidAPI Alternative", "Enterprise API Hub & Testing", "Migrate from RapidAPI", "Modern API Platform", "Complete API Workspace"],
            'descriptions': ["The ultimate alternative to RapidAPI. Manage, test, and mock your APIs with ease.", "Seamlessly migrate from RapidAPI today. Experience a modern API workspace."]
        })
        
    if 'Google-Sa-CP-ID' in camp_res_map:
        ag_data.append({
            'campaign': 'Google-Sa-CP-ID',
            'name': 'ID-Native-API',
            'kws': ["alternatif postman gratis", "alat pengujian api"],
            'url': 'https://apidog.com/',
            'headlines': ["Alternatif Postman Terbaik", "Coba Apidog Gratis", "Alat Pengujian API", "Desain API Lebih Cepat", "Platform API Lengkap"],
            'descriptions': ["Beralih dari Postman hari ini. Pengujian API tanpa batas dan gratis.", "Platform API terintegrasi untuk seluruh tim pengembangan Anda."]
        })

    if not ag_data:
        print("No campaigns found for expansion.")
        return

    # Fetch Ad Groups since they were already created
    ag_res_map = {}
    for g in ag_data:
        q_ag = f"SELECT ad_group.resource_name FROM ad_group WHERE ad_group.name = '{g['name']}' AND campaign.id = {camp_res_map[g['campaign']].split('/')[-1]}"
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag):
            for row in batch.results:
                ag_res_map[g['name']] = row.ad_group.resource_name
                break

    # Create Keywords
    kw_ops = []
    for g in ag_data:
        ag_res = ag_res_map.get(g['name'])
        if not ag_res: continue
        for kw_text in g['kws']:
            op = client.get_type("AdGroupCriterionOperation")
            crit = op.create
            crit.ad_group = ag_res
            crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            crit.keyword.text = kw_text
            crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            kw_ops.append(op)
            
    if kw_ops:
        try:
            kw_request = client.get_type("MutateAdGroupCriteriaRequest")
            kw_request.customer_id = CUSTOMER_ID
            kw_request.operations = kw_ops
            kw_request.partial_failure = True
            kw_resp = agc_service.mutate_ad_group_criteria(request=kw_request)
            print("Keywords processed with partial_failure.")
        except GoogleAdsException as ex:
            print(f"Failed to create keywords: {ex}")

    # Create RSAs
    print("RSAs were already created in previous run. Skipping.")
    print("Execution complete!")

if __name__ == '__main__':
    execute()
