# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

SECTION_1_KEYWORDS = {
    "Google-Sa-CP-ES": ["alternativas a postman", "alternativa a postman gratis", "postman gratis", "postman espanol"],
    "Google-Sa-CP-MX": ["alternativas a postman", "postman mexico gratis", "probador de api gratis", "alternativa postman gratis"],
    "Google-Sa-CP-AR": ["بديل postman", "اختبار api مجاني", "postman alternative arabic", "postman free alternative"],
    "Google-Sa-CP-PT": ["alternativa ao postman", "testar api online gratis", "postman portugues", "alternativa postman brasil"],
    "Google-Sa-CP-JP": ["postman 代替", "api テスト ツール", "postman 日本語", "apidog 日本語"],
    "Google-Sa-CP-KR": ["postman 대체", "api 테스트 툴", "postman 사용법", "apidog 한국어"],
    "Google-Sa-CP-TW": ["postman 替代方案", "api 測試工具 免費", "postman 中文版", "apidog 繁體中文"],
    "Google-Sa-CP-VN": ["thay thế postman", "công cụ test api miễn phí", "postman tiếng việt", "apidog tiếng việt"],
    "Google-Sa-CP-ID": ["alternatif postman", "aplikasi testing api gratis", "postman indonesia", "apidog indonesia"],
    "Google-Sa-CP-DE": ["postman alternative deutsch", "api testen kostenlos", "postman ersatz", "postman alternative deutschland"],
    "Google-Sa-CP-FR": ["alternative a postman", "outil test api gratuit", "postman en francais", "alternative postman france"],
    "Google-Sa-CP-TR": ["postman alternatifi", "ücretsiz api test aracı", "postman türkçe", "apidog türkiye"]
}

def execute_keywords_upload():
    print("==================================================================")
    print("🚀 ADDING ALL 96 KEYWORDS TO 12 AD GROUPS RIGHT NOW")
    print("==================================================================")
    
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ad_group_criterion_service = client.get_service('AdGroupCriterionService')

    # 1. Fetch Ad Group IDs
    query = """
        SELECT ad_group.id, ad_group.name, campaign.name
        FROM ad_group
        WHERE ad_group.name LIKE 'Postman-Alternative-%-2026'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    ag_map = {}
    for batch in stream:
        for row in batch.results:
            ag_map[row.campaign.name] = {
                "ag_id": row.ad_group.id,
                "ag_name": row.ad_group.name
            }
            print(f"Mapped Campaign '{row.campaign.name}' -> Ad Group '{row.ad_group.name}' (ID: {row.ad_group.id})")

    # 2. Build Keyword Operations
    kw_ops = []
    total_added = 0

    for camp_name, words in SECTION_1_KEYWORDS.items():
        if camp_name not in ag_map:
            print(f"⚠️ Warning: Campaign '{camp_name}' has no matching 2026 Ad Group!")
            continue
            
        ag_id = ag_map[camp_name]["ag_id"]
        ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)

        for kw_text in words:
            # Phrase match
            op_p = client.get_type('AdGroupCriterionOperation')
            agc_p = op_p.create
            agc_p.ad_group = ag_path
            agc_p.keyword.text = kw_text
            agc_p.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            agc_p.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(op_p)
            total_added += 1

            # Exact match
            op_e = client.get_type('AdGroupCriterionOperation')
            agc_e = op_e.create
            agc_e.ad_group = ag_path
            agc_e.keyword.text = kw_text
            agc_e.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            agc_e.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(op_e)
            total_added += 1

    print(f"\n>>> Submitting {len(kw_ops)} keyword creation operations to Google Ads API...")

    if kw_ops:
        request = client.get_type('MutateAdGroupCriteriaRequest')
        request.customer_id = CUSTOMER_ID
        request.operations.extend(kw_ops)
        request.partial_failure = True
        
        response = ad_group_criterion_service.mutate_ad_group_criteria(request=request)
        print(f"\n✅ SUCCESS: Successfully uploaded {total_added} Phrase & Exact keywords across 12 Ad Groups!")
    return True

def main():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}...")
            if execute_keywords_upload():
                break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(2)

if __name__ == '__main__':
    main()
