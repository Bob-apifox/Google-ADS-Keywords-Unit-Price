import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

PAUSE_TARGETS = [
    "Google-Sa-CP-DE",
    "Google-Sa-NextGen-API-Docs-Global",
    "Google-Sa-Comp-StaticDocs-Global"
]

DIAGNOSTIC_CAMPAIGNS = [
    "Google-Sa-Stoplight-Global",
    "Google-Sa-Insomnia-Global",
    "Google-Sa-Bruno-Global",
    "Google-Sa-CLI-Global",
    "Google-Sa-CLI-Terminal-Global",
    "Google-Sa-Readme-Global",
    "Google-Sa-Mintlify-Global"
]

def pause_approved_campaigns(client, customer_id):
    print("==========================================================================")
    print("[1. PAUSING THE 3 APPROVED CAMPAIGNS (CP-DE, NextGen, StaticDocs)]")
    print("==========================================================================")
    ga_service = client.get_service("GoogleAdsService")
    campaign_service = client.get_service("CampaignService")

    names_str = ", ".join([f"'{n}'" for n in PAUSE_TARGETS])
    q = f"SELECT campaign.id, campaign.name, campaign.resource_name FROM campaign WHERE campaign.name IN ({names_str})"
    ops = []
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            op = client.get_type("CampaignOperation")
            c = op.update
            c.resource_name = row.campaign.resource_name
            c.status = client.enums.CampaignStatusEnum.PAUSED
            client.copy_from(op.update_mask, protobuf_helpers.field_mask(None, c._pb))
            ops.append(op)
            print(f"Pausing: {row.campaign.name} ({row.campaign.resource_name})")

    if ops:
        try:
            campaign_service.mutate_campaigns(customer_id=customer_id, operations=ops)
            print("[SUCCESS] The 3 campaigns are now PAUSED live!")
        except Exception as e:
            print(f"[ERROR] Pausing: {e}")

def audit_search_terms_and_keywords(client, customer_id):
    print("\n==========================================================================")
    print("[2. DEEP SEARCH TERM & KEYWORD AUDIT (PAST 14 DAYS)]")
    print("==========================================================================")
    ga_service = client.get_service("GoogleAdsService")

    # 1. Search Terms (Past 14 Days)
    names_str = ", ".join([f"'{n}'" for n in DIAGNOSTIC_CAMPAIGNS])
    q_st = f"""
        SELECT
            campaign.name,
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.clicks,
            metrics.impressions,
            metrics.conversions
        FROM search_term_view
        WHERE campaign.name IN ({names_str})
          AND segments.date DURING LAST_14_DAYS
          AND metrics.cost_micros > 2000000
        ORDER BY metrics.cost_micros DESC
    """
    st_by_camp = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_st):
        for row in batch.results:
            cname = row.campaign.name
            st = row.search_term_view.search_term
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            conv = row.metrics.conversions
            if cname not in st_by_camp:
                st_by_camp[cname] = []
            st_by_camp[cname].append((st, cost, clicks, conv))

    # 2. Keywords in Campaigns
    q_kw = f"""
        SELECT
            campaign.name,
            ad_group_criterion.keyword.text,
            ad_group_criterion.keyword.match_type,
            ad_group_criterion.status,
            metrics.cost_micros,
            metrics.clicks
        FROM keyword_view
        WHERE campaign.name IN ({names_str})
          AND segments.date DURING LAST_14_DAYS
          AND ad_group_criterion.status = 'ENABLED'
        ORDER BY metrics.cost_micros DESC
    """
    kw_by_camp = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_kw):
        for row in batch.results:
            cname = row.campaign.name
            ktext = row.ad_group_criterion.keyword.text
            mtype = row.ad_group_criterion.keyword.match_type.name
            cost = row.metrics.cost_micros / 1000000.0
            clicks = row.metrics.clicks
            if cname not in kw_by_camp:
                kw_by_camp[cname] = []
            kw_by_camp[cname].append((ktext, mtype, cost, clicks))

    # 3. Ads and Landing Pages
    q_ads = f"""
        SELECT
            campaign.name,
            ad_group_ad.ad.id,
            ad_group_ad.ad.final_urls,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions
        FROM ad_group_ad
        WHERE campaign.name IN ({names_str})
          AND ad_group_ad.status = 'ENABLED'
    """
    ads_by_camp = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q_ads):
        for row in batch.results:
            cname = row.campaign.name
            urls = list(row.ad_group_ad.ad.final_urls)
            hls = [h.text for h in row.ad_group_ad.ad.responsive_search_ad.headlines]
            descs = [d.text for d in row.ad_group_ad.ad.responsive_search_ad.descriptions]
            if cname not in ads_by_camp:
                ads_by_camp[cname] = []
            ads_by_camp[cname].append((urls, hls, descs))

    for cname in DIAGNOSTIC_CAMPAIGNS:
        print(f"\n--------------------------------------------------------------------------")
        print(f"📌 CAMPAIGN: {cname}")
        print(f"--------------------------------------------------------------------------")
        
        # Print Landing Page & Sample Copy
        if cname in ads_by_camp and ads_by_camp[cname]:
            urls, hls, descs = ads_by_camp[cname][0]
            print(f"  [Landing URL]: {urls[0] if urls else 'N/A'}")
            print(f"  [Sample Headlines]: {hls[:4]}")
            print(f"  [Sample Descs]: {descs[:2]}")

        # Print Top Spending Keywords
        print(f"  [Top Active Keywords (Past 14 Days)]:")
        kws = kw_by_camp.get(cname, [])
        for k in kws[:5]:
            print(f"    - [{k[1]}] '{k[0]}' | Spend: ${k[2]:.2f} | Clicks: {k[3]}")

        # Print Top Search Terms
        print(f"  [Top High-Cost Search Terms (Past 14 Days)]:")
        sts = st_by_camp.get(cname, [])
        if not sts:
            print("    (No search terms with >$2.00 spend)")
        for st in sts[:8]:
            print(f"    - Term: '{st[0]:<35}' | Spend: ${st[1]:<5.2f} | Clicks: {st[2]:<3} | Convs: {st[3]:.1f}")

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    pause_approved_campaigns(client, CUSTOMER_ID)
    audit_search_terms_and_keywords(client, CUSTOMER_ID)

if __name__ == '__main__':
    main()
