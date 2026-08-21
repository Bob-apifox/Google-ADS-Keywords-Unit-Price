import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")

    print("==========================================================================")
    print("[1. SEARCH IMPRESSION SHARE LOSS ANALYSIS (LAST 7 DAYS)]")
    print("==========================================================================")

    q_is = """
        SELECT
            campaign.name,
            campaign_budget.amount_micros,
            metrics.cost_micros,
            metrics.conversions,
            metrics.search_impression_share,
            metrics.search_budget_lost_impression_share,
            metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE campaign.status = 'ENABLED'
          AND segments.date >= '2026-08-05'
          AND segments.date <= '2026-08-11'
          AND metrics.cost_micros > 20000000
        ORDER BY metrics.cost_micros DESC
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_is):
        for row in batch.results:
            cname = row.campaign.name
            cost = row.metrics.cost_micros / 1000000.0
            conv = row.metrics.conversions
            cpa = cost / conv if conv > 0 else 0.0
            sis = row.metrics.search_impression_share
            lost_b = row.metrics.search_budget_lost_impression_share
            lost_r = row.metrics.search_rank_lost_impression_share
            
            sis_str = f"{sis*100:.1f}%" if sis else "N/A"
            lost_b_str = f"{lost_b*100:.1f}%" if lost_b else "N/A"
            lost_r_str = f"{lost_r*100:.1f}%" if lost_r else "N/A"
            
            print(f"[{cname:<35}] Spend: ${cost:<7.2f} | Convs: {conv:<5.1f} | CPA: ${cpa:<5.2f} | IS: {sis_str:<6} | Lost(Budget): {lost_b_str:<6} | Lost(Rank): {lost_r_str}")

    print("\n==========================================================================")
    print("[2. HIGH-CONVERTING SEARCH TERMS NOT YET HARVESTED AS EXACT KEYWORDS]")
    print("==========================================================================")

    q_st = """
        SELECT
            campaign.name,
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks,
            metrics.conversions
        FROM search_term_view
        WHERE segments.date >= '2026-08-05'
          AND segments.date <= '2026-08-11'
          AND metrics.conversions >= 3
        ORDER BY metrics.conversions DESC
        LIMIT 30
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_st):
        for row in batch.results:
            cname = row.campaign.name
            st = row.search_term_view.search_term
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            conv = row.metrics.conversions
            cpa = cost / conv if conv > 0 else 0.0
            print(f"[{cname:<30}] Term: '{st:<35}' | Convs: {conv:<4.1f} | Spend: ${cost:<6.2f} | CPA: ${cpa:.2f}")

    print("\n==========================================================================")
    print("[3. WHY CATEGORY-COMPETITOR HAS ONLY $0.57 SPEND (UNDER-DELIVERING)]")
    print("==========================================================================")
    q_cat = """
        SELECT
            ad_group.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks
        FROM keyword_view
        WHERE campaign.name = 'Google-Sa-Category-Competitor-Global'
          AND segments.date >= '2026-08-05'
          AND segments.date <= '2026-08-11'
    """
    for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_cat):
        for row in batch.results:
            ag = row.ad_group.name
            kw = row.ad_group_criterion.keyword.text
            mt = row.ad_group_criterion.keyword.match_type.name
            impr = row.metrics.impressions
            clicks = row.metrics.clicks
            cost = row.metrics.cost_micros / 1000000.0
            print(f"Group: {ag:<25} | Keyword: {kw:<30} ({mt}) | Impr: {impr:<4} | Clicks: {clicks} | Cost: ${cost:.2f}")

if __name__ == '__main__':
    main()
