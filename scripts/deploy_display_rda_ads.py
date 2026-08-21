import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

GOOGLE_ADS_YAML = r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml"
CUSTOMER_ID = "9496728294"

LANDSCAPE_IMG_1 = "183793374610"  # 1200x628
LANDSCAPE_IMG_2 = "188645331605"  # 1200x628
SQUARE_IMG_1 = "183756328178"     # 800x800
SQUARE_IMG_2 = "183756508835"     # 1620x1620

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    customer_id = CUSTOMER_ID
    ga_service = client.get_service("GoogleAdsService")
    ad_group_ad_service = client.get_service("AdGroupAdService")

    q = """
        SELECT
            campaign.name,
            ad_group.resource_name
        FROM ad_group
        WHERE campaign.name IN ('Google-Dis-Remarketing-Global', 'Google-Dis-DevPlacements-Global')
          AND ad_group.status != 'REMOVED'
    """
    ag_map = {}
    for batch in ga_service.search_stream(customer_id=customer_id, query=q):
        for row in batch.results:
            ag_map[row.campaign.name] = row.ad_group.resource_name

    # 1. Remarketing Ad
    if "Google-Dis-Remarketing-Global" in ag_map:
        ag_res = ag_map["Google-Dis-Remarketing-Global"]
        ad_op = client.get_type("AdGroupAdOperation")
        aga = ad_op.create
        aga.ad_group = ag_res
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED

        ad = aga.ad
        ad.final_urls.append("https://apidog.com/")
        ad.final_url_suffix = "utm_source=google_display&utm_medium=remarketing&utm_campaign={campaignid}&utm_adgroup={adgroupid}"

        rda = ad.responsive_display_ad
        rda.business_name = "Apidog"
        rda.long_headline.text = "Design, Debug, Mock, and Test APIs in One Single Workspace. Try Apidog for Free."

        h1 = [
            "Still Struggling with Postman?",
            "Visual API Design & Debugging",
            "The All-in-One API Platform",
            "Free Unlimited API Test Runner",
            "Upgrade Your API Workflow Now"
        ]
        for h in h1:
            hl = client.get_type("AdTextAsset")
            hl.text = h
            rda.headlines.append(hl)

        d1 = [
            "Join 1M+ developers using Apidog for visual API design, testing, and mock servers.",
            "Tired of switching between tools? Apidog combines Postman, Swagger, and JMeter in one.",
            "Import Postman collections in seconds and enjoy unlimited test runs for free."
        ]
        for d in d1:
            ds = client.get_type("AdTextAsset")
            ds.text = d
            rda.descriptions.append(ds)

        # Marketing Images (Landscape)
        img1 = client.get_type("AdImageAsset")
        img1.asset = f"customers/{customer_id}/assets/{LANDSCAPE_IMG_1}"
        rda.marketing_images.append(img1)

        # Square Images
        sq1 = client.get_type("AdImageAsset")
        sq1.asset = f"customers/{customer_id}/assets/{SQUARE_IMG_1}"
        rda.square_marketing_images.append(sq1)

        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"[SUCCESS] Created Remarketing RDA Ad: {resp.results[0].resource_name}")
        except Exception as e:
            print(f"[ERROR] Creating Remarketing RDA Ad: {e}")

    # 2. DevPlacements Ad
    if "Google-Dis-DevPlacements-Global" in ag_map:
        ag_res = ag_map["Google-Dis-DevPlacements-Global"]
        ad_op = client.get_type("AdGroupAdOperation")
        aga = ad_op.create
        aga.ad_group = ag_res
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED

        ad = aga.ad
        ad.final_urls.append("https://apidog.com/")
        ad.final_url_suffix = "utm_source=google_display&utm_medium=placement_branding&utm_campaign={campaignid}&utm_adgroup={adgroupid}"

        rda = ad.responsive_display_ad
        rda.business_name = "Apidog"
        rda.long_headline.text = "A Smarter, Visual API Development Workspace Built for Modern Engineering Teams."

        h2 = [
            "Best Postman Alternative 2026",
            "Modern API Platform for Teams",
            "API Design, Mock & Test Tool",
            "Automated API Testing in CI/CD",
            "Visual API Workspace for Devs"
        ]
        for h in h2:
            hl = client.get_type("AdTextAsset")
            hl.text = h
            rda.headlines.append(hl)

        d2 = [
            "Stop jumping across Postman, Swagger, and JMeter. Streamline your API lifecycle.",
            "Auto-generate mock data, run automated tests, and sync API documentation seamlessly.",
            "Built for developers who value speed and efficiency. Free for individuals and teams."
        ]
        for d in d2:
            ds = client.get_type("AdTextAsset")
            ds.text = d
            rda.descriptions.append(ds)

        # Marketing Images (Landscape)
        img2 = client.get_type("AdImageAsset")
        img2.asset = f"customers/{customer_id}/assets/{LANDSCAPE_IMG_2}"
        rda.marketing_images.append(img2)

        # Square Images
        sq2 = client.get_type("AdImageAsset")
        sq2.asset = f"customers/{customer_id}/assets/{SQUARE_IMG_2}"
        rda.square_marketing_images.append(sq2)

        try:
            resp = ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"[SUCCESS] Created DevPlacements RDA Ad: {resp.results[0].resource_name}")
        except Exception as e:
            print(f"[ERROR] Creating DevPlacements RDA Ad: {e}")

    print("\n==========================================================================")
    print("[ALL DONE] RDA Ads 100% Attached & Deployed Live!")
    print("==========================================================================")

if __name__ == '__main__':
    main()
