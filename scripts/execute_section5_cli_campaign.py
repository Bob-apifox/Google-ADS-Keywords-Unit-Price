import os
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'
CAMPAIGN_NAME = 'Google-Sa-CLI-Terminal-Global'

def execute():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service('GoogleAdsService')
        
        # 1. Skip Campaign fetch, use existing AdGroups directly
        ag_res_map = {
            'CLI-Automated-Testing': 'customers/9496728294/adGroups/198846510613',
            'CLI-Alternatives': 'customers/9496728294/adGroups/198846510653'
        }

        # 4. Create RSAs
        ad_service = client.get_service('AdGroupAdService')
        rsa_ops = []
        
        headlines = [
            "The Ultimate API CLI Tool", "Run API Tests in CI/CD", "Better Than Newman CLI",
            "Best Postman CLI Alternative", "Terminal-Based API Testing", "Command Line API Client",
            "Automate Your API Tests", "Perfect CI/CD Integration", "Zero UI Required",
            "100% Terminal Efficiency", "Lightweight API CLI", "Automate API Documentation",
            "Fast API Test Execution", "API Testing for DevOps", "Try Apidog CLI for Free"
        ]
        descriptions = [
            "Zero UI required. Execute API tests, generate mocks & deploy directly from your terminal.",
            "Seamlessly integrates with Jenkins, GitHub Actions & GitLab. Master your CI/CD pipeline.",
            "The perfect Newman & Postman CLI alternative. Lightweight, fast & highly customizable.",
            "Built for DevOps and backend engineers. Run complex test suites inside the command line."
        ]
        
        for g, ag_res in ag_res_map.items():
            op = client.get_type("AdGroupAdOperation")
            ad_group_ad = op.create
            ad_group_ad.ad_group = ag_res
            ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
            ad_group_ad.ad.final_urls.append("https://apidog.com/apidog-cli/")
            ad_group_ad.ad.tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium=ads_sa&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"
            
            for h in headlines:
                asset = client.get_type("AdTextAsset")
                asset.text = h
                ad_group_ad.ad.responsive_search_ad.headlines.append(asset)
                
            for d in descriptions:
                asset = client.get_type("AdTextAsset")
                asset.text = d
                ad_group_ad.ad.responsive_search_ad.descriptions.append(asset)
                
            rsa_ops.append(op)
            
        print("Creating RSAs...")
        rsa_resp = ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=rsa_ops)
        print(f"Created {len(rsa_resp.results)} RSAs.")
        print("Done! Upload successful.")

    except GoogleAdsException as ex:
        print(f"GoogleAdsException occurred: {ex}")
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")

if __name__ == '__main__':
    execute()
