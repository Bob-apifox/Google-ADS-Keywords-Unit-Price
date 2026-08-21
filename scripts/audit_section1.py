# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try: sys.stdout.reconfigure(encoding='utf-8')
except: pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

target_campaigns = [
    "Google-Sa-CP-ES", "Google-Sa-CP-MX", "Google-Sa-CP-AR", "Google-Sa-CP-PT",
    "Google-Sa-CP-JP", "Google-Sa-CP-KR", "Google-Sa-CP-TW", "Google-Sa-CP-VN",
    "Google-Sa-CP-ID", "Google-Sa-CP-DE", "Google-Sa-CP-FR", "Google-Sa-CP-TR",
    "Google-Sa-CP-ar"
]

def run_audit():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    report = {}
    
    # 1. Campaigns & Budgets
    q_camp = """
        SELECT campaign.id, campaign.name, campaign.status, campaign_budget.amount_micros
        FROM campaign
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND campaign.status != 'REMOVED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            if any(tc.lower() in c_name.lower() for tc in target_campaigns):
                if c_name not in report:
                    report[c_name] = {"budget": row.campaign_budget.amount_micros / 1000000 if row.campaign_budget else 0, "status": row.campaign.status.name, "ad_groups": {}}

    # 2. Ad Groups & CPA
    q_ag = """
        SELECT ad_group.id, ad_group.name, ad_group.status, ad_group.target_cpa_micros, campaign.name, campaign.target_cpa.target_cpa_micros
        FROM ad_group
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            if c_name in report:
                ag_name = row.ad_group.name
                cpa = row.ad_group.target_cpa_micros
                if not cpa: # fallback to campaign level if not set at ad group
                    cpa = row.campaign.target_cpa.target_cpa_micros
                report[c_name]["ad_groups"][ag_name] = {
                    "cpa": cpa / 1000000 if cpa else 0,
                    "ads": [],
                    "keywords": []
                }

    # 3. Ads (Creatives)
    q_ad = """
        SELECT ad_group_ad.ad.id, ad_group.name, campaign.name, ad_group_ad.status, 
               ad_group_ad.policy_summary.approval_status, 
               ad_group_ad.ad.responsive_search_ad.headlines
        FROM ad_group_ad
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED' AND ad_group_ad.status != 'REMOVED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ad)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            if c_name in report and ag_name in report[c_name]["ad_groups"]:
                ad = row.ad_group_ad
                headlines = [hl.text for hl in ad.ad.responsive_search_ad.headlines]
                report[c_name]["ad_groups"][ag_name]["ads"].append({
                    "id": ad.ad.id,
                    "status": ad.status.name,
                    "approval": ad.policy_summary.approval_status.name if ad.policy_summary else "UNKNOWN",
                    "headlines": headlines[:3] # just take first 3 to verify personalization
                })

    # 4. Keywords
    q_kw = """
        SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group.name, campaign.name
        FROM ad_group_criterion
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED' AND ad_group_criterion.status = 'ENABLED' AND ad_group_criterion.type = 'KEYWORD'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_kw)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            if c_name in report and ag_name in report[c_name]["ad_groups"]:
                kw = row.ad_group_criterion
                report[c_name]["ad_groups"][ag_name]["keywords"].append(kw.keyword.text)

    # 5. Geo Targeting (Locations)
    q_geo = """
        SELECT campaign.name, campaign_criterion.location.geo_target_constant
        FROM campaign_criterion
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND campaign_criterion.type = 'LOCATION'
    """
    geo_ids = set()
    camp_geos = {}
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_geo)
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            geo_id = row.campaign_criterion.location.geo_target_constant.split('/')[-1]
            if c_name not in camp_geos:
                camp_geos[c_name] = []
            camp_geos[c_name].append(geo_id)
            geo_ids.add(geo_id)
            
    # Resolve geo IDs to names
    geo_names = {}
    if geo_ids:
        q_geo_names = f"""
            SELECT geo_target_constant.id, geo_target_constant.canonical_name, geo_target_constant.country_code
            FROM geo_target_constant
            WHERE geo_target_constant.id IN ({",".join(geo_ids)})
        """
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_geo_names)
        for batch in stream:
            for row in batch.results:
                geo_names[str(row.geo_target_constant.id)] = f"{row.geo_target_constant.canonical_name} ({row.geo_target_constant.country_code})"
                
    for c_name, c_data in report.items():
        if c_name in camp_geos:
            report[c_name]["targets"] = [geo_names.get(gid, gid) for gid in camp_geos[c_name]]
        else:
            report[c_name]["targets"] = []

    with open('d:/Apidog Work/Google ADS Keywords Unit Price/data/audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        
    print("Audit finished. Saved to data/audit_report.json")
    return True

def main():
    max_retries = 10
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            if run_audit():
                break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == '__main__':
    main()
