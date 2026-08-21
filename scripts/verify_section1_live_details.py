# -*- coding: utf-8 -*-
import os
import sys
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

campaign_ids = [
    21995819717, 21995977112, 23139757330, 22261650381, 21965514943,
    22309414047, 23264160392, 22374204671, 22451766179, 22367960103,
    23027715066, 23047433007
]

def main():
    print("==================================================================")
    print("🔍 VERIFYING LIVE GOOGLE ADS STATE FOR 12 CAMPAIGNS")
    print("==================================================================")
    
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    ids_str = ", ".join(map(str, campaign_ids))
    
    # 1. Query Campaigns
    print("\n--- 1. CAMPAIGN STATUS ---")
    query_camps = f"SELECT campaign.id, campaign.name, campaign.status, campaign.final_url_suffix FROM campaign WHERE campaign.id IN ({ids_str})"
    stream_camps = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_camps)
    for b in stream_camps:
        for r in b.results:
            print(f"Campaign: '{r.campaign.name}' (ID: {r.campaign.id}) | Status: {r.campaign.status.name} | Suffix: '{r.campaign.final_url_suffix}'")

    # 2. Query Ad Groups
    print("\n--- 2. AD GROUPS IN CAMPAIGNS ---")
    query_ags = f"SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id, campaign.name FROM ad_group WHERE campaign.id IN ({ids_str})"
    stream_ags = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ags)
    ag_ids = []
    for b in stream_ags:
        for r in b.results:
            ag_ids.append(r.ad_group.id)
            print(f"Campaign: '{r.campaign.name}' -> AdGroup: '{r.ad_group.name}' (ID: {r.ad_group.id}) | Status: {r.ad_group.status.name}")

    if not ag_ids:
        print("❌ NO AD GROUPS FOUND!")
        return

    ag_ids_str = ", ".join(map(str, ag_ids))

    # 3. Query Keywords
    print("\n--- 3. KEYWORDS IN AD GROUPS ---")
    query_kws = f"SELECT ad_group.id, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status FROM ad_group_criterion WHERE ad_group.id IN ({ag_ids_str}) AND ad_group_criterion.type = 'KEYWORD'"
    stream_kws = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_kws)
    kw_count = 0
    for b in stream_kws:
        for r in b.results:
            kw_count += 1
            if kw_count <= 25:
                print(f"AdGroup ID {r.ad_group.id} -> Keyword: '{r.ad_group_criterion.keyword.text}' ({r.ad_group_criterion.keyword.match_type.name}) | Status: {r.ad_group_criterion.status.name}")
    print(f"Total Keywords found: {kw_count}")

    # 4. Query Ads
    print("\n--- 4. ADS / RSAs IN AD GROUPS ---")
    query_ads = f"SELECT ad_group.id, ad_group_ad.ad.id, ad_group_ad.ad.type, ad_group_ad.status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE ad_group.id IN ({ag_ids_str})"
    stream_ads = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query_ads)
    ad_count = 0
    for b in stream_ads:
        for r in b.results:
            ad_count += 1
            urls = list(r.ad_group_ad.ad.final_urls)
            print(f"AdGroup ID {r.ad_group.id} -> Ad ID: {r.ad_group_ad.ad.id} ({r.ad_group_ad.ad.type.name}) | Status: {r.ad_group_ad.status.name} | Final URLs: {urls}")
    print(f"Total Ads found: {ad_count}")

if __name__ == '__main__':
    main()
