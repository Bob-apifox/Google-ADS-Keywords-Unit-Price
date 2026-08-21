# -*- coding: utf-8 -*-
import os
import json
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v23.enums.types.keyword_match_type import KeywordMatchTypeEnum

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

campaign_ids = [22061425619, 22067541248, 22892634645, 22923613652, 23030065589, 
                23320166856, 23347684482, 23376992548, 23716128367, 23770423434, 23921795178]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    # 1. Fetch Campaign Name -> Campaign ID mapping
    ids_str = ', '.join(map(str, campaign_ids))
    query = f'''
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.id IN ({ids_str})
    '''
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    name_to_id = {}
    for batch in stream:
        for row in batch.results:
            name_to_id[row.campaign.name] = row.campaign.id

    # 2. Process search_terms.json
    suspicious_words = [
        'interview', 'salary', 'jobs', 'career', 'resume', 'internship',
        'exam', 'certification', 'training', 'course', 'class', 'syllabus',
        'meaning', 'definition', 'what is', 'how to', 'tutorial',
        'crack', 'torrent', 'nulled', 'free download full version',
        'reddit', 'youtube', 'github issues', 'vs', 'difference between'
    ]

    with open('search_terms.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    campaign_negatives = {}
    
    for row in data:
        term = row['search_term'].lower()
        conv = row['conversions']
        camp_name = row['campaign']
        
        if camp_name not in name_to_id:
            continue
            
        camp_id = name_to_id[camp_name]
        
        if camp_id not in campaign_negatives:
            campaign_negatives[camp_id] = set()
            
        if conv == 0:
            for w in suspicious_words:
                if w in term:
                    campaign_negatives[camp_id].add(w)

    # --- Add specific negatives based on 07-13 optimization plan ---
    specific_negatives = {
        # Design-Global
        22132696993: ["app create", "build app", "creer un logiciel", "mobile app", "web app to mobile app", "base44", "rork max", "app design_guidelines json", "kotlin multiplatform developer", "apidog شرح"],
        # API Editor-Global
        23376992548: ["playwright", "camunda", "niotron", "pwa builder", "computer software", "retool com api generator", "flowgorithm online", "crear programa", "online software", "api online", "traycer", "rocket com", "openapi 3.1"],
        # CLI-Global
        23974416637: ["web alternative", "offline alternative", "free api tools like", "postman free version", "best alternative for postman", "online postman", "apidog cli", "alternative of postman", "postman alternative offline"],
        # Readme-Global
        23030065589: ["mermaid js", "dillinger io", "kotlin", "draw io", "app making ai", "lovable dev", "fast api", "markitdown online", "documentation ai", "whatsapp business api", "git for windows", "node js lts", "bubble", "pip install reportlab", "google firebase studio", "redoc", "firebase studio", "next js ai"],
        # Mintlify-Global
        23320166856: ["intellij idea", "pycharm", "run code", "ia para generar codigos", "whimsical", "codepad", "burp suite", "bruno api", "mobile ides", "von dev ai", "intellij idea community edition", "online visual studio", "website coding", "electron", "next js", "rest client online", "app making", "templafy", "online rest api testing", "platform maker ai", "ia para generar codigos de programacion", "redoc"],
        # Swagger-Global
        22923613652: ["swaggerhub", "openapi documentation"],
        # RapidAPI-Global
        22936440663: ["consumir api rest online", "teste de api online", "rapidapi marketplace"],
        # Func-MultiProtocol-Global
        23981407167: ["websocket king"],
        # Scalar-Global
        23405649492: ["api reader online", "api check", "n8n automation", "proxy integration", "oauth 2.0 setup"],
        # Stoplight-Global
        22892634645: ["ocr api", "app creating software", "browser automation studio", "pnpm install", "autogpt", "code visualstudio com", "openrpa"],
        # Solutions-Multi-Protocol-Global
        23712917923: ["locust", "ide software", "ai api tester", "https k6 io cloud", "como criar api", "dev essentials", "webpagetest", "webhooks", "api testing tool", "coding software", "web hook", "check api online", "integrated development environment ide", "devtools", "online http request sender", "testingbot"],
        # Insomnia-Global
        22806818611: ["firebase studio", "api maker", "x request id", "wiremock", "playwright api testing"],
        # DSA-Postman-Global
        22058259794: ["api dog vs postman", "environment variables", "visual code"],
        # The Great Migration-26
        23435786807: ["code visualstudio com", "react native app", "from idea to app instantly"],
        # Bump.sh-Global
        23329106566: ["opencode", "hugging face", "markdown it npm", "api dots", "amazon q developer"],
        # Mock-Global
        22067541248: ["glide apps", "appetize io", "v0 by vercel", "nocodb", "browserstack", "api runner online", "insomnia community edition", "api chai", "google api_core", "create mock api online", "backend"],
        # Doc-Global
        22061425619: ["electron", "datadog api documentation", "openrouter", "read the docs alternatives"],
        # SpecFirst-Global
        23921795178: ["zapier ai", "backendless", "latenode", "hoppscotch download", "free api testing tools", "apidogs", "backend api", "free http client", "swagger api", "api dog"],
        # Bruno-Global
        23347684482: ["openrouter api", "amazon q developer", "odoo community edition", "firebase studio", "make com", "workflow", "https ngrok com", "bruno mac", "service role key", "connexion redirect_uri"],
        # MCP-Infrastructure
        23864356298: ["cursor a", "cursor claude", "exa mcp server"],
        # LLM-Benchmarking
        23868709405: ["ai dev", "coding agents", "llama", "https openrouter ai"],
        # Category-Competitor
        23756781032: ["devtools"],
        # Openapi-Global
        22967853243: ["reportlab", "apidock", "ai agent", "cline", "appy pie", "glide app", "ذكاء اصطناعي مفتوح المصدر"]
    }
    
    for camp_id, words in specific_negatives.items():
        if camp_id not in campaign_negatives:
            campaign_negatives[camp_id] = set()
        for word in words:
            campaign_negatives[camp_id].add(word)
                    
    # 3. Create operations
    cc_service = client.get_service('CampaignCriterionService')
    operations = []
    
    for camp_id, neg_words in campaign_negatives.items():
        for word in neg_words:
            cc_op = client.get_type('CampaignCriterionOperation')
            cc_op.create.campaign = ga_service.campaign_path(CUSTOMER_ID, camp_id)
            cc_op.create.negative = True
            cc_op.create.keyword.text = word
            cc_op.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            operations.append(cc_op)

    print(f'Prepared {len(operations)} negative keyword operations.')

    if operations:
        try:
            request = client.get_type('MutateCampaignCriteriaRequest')
            request.customer_id = CUSTOMER_ID
            request.operations.extend(operations)
            request.partial_failure = True
            
            response = cc_service.mutate_campaign_criteria(request=request)
            print(f'Successfully added negative keywords!')
        except Exception as e:
            print(f'Error adding negative keywords: {e}')
    else:
        print('No negative keywords to add.')

if __name__ == '__main__':
    main()
