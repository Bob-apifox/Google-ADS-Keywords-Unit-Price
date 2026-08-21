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
CAMPAIGN_NAME = 'Google-Sa-Testing-Global'

def execute():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service('GoogleAdsService')
        
        # 1. Fetch Campaign
        q_camp = f"SELECT campaign.id, campaign.resource_name FROM campaign WHERE campaign.name = '{CAMPAIGN_NAME}'"
        camp_res = None
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_camp):
            for row in batch.results:
                camp_res = row.campaign.resource_name
                print(f"Found campaign: {CAMPAIGN_NAME} (Resource: {camp_res})")
                break
                
        if not camp_res:
            print(f"Could not find campaign: {CAMPAIGN_NAME}")
            return

        # 2. Create Ad Groups
        ag_service = client.get_service('AdGroupService')
        ag_ops = []
        
        ad_groups_data = [
            {'name': 'Testing-Advanced-Workflows'},
            {'name': 'Testing-Security-Auth'}
        ]
        
        for g in ad_groups_data:
            op = client.get_type("AdGroupOperation")
            ag = op.create
            ag.campaign = camp_res
            ag.name = g['name']
            ag.status = client.enums.AdGroupStatusEnum.ENABLED
            ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
            ag.cpc_bid_micros = 1000000
            ag_ops.append(op)
            
        print(f"Creating AdGroups...")
        ag_resp = ag_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=ag_ops)
        ag_res_map = {}
        for i, res in enumerate(ag_resp.results):
            ag_name = ad_groups_data[i]['name']
            ag_res_map[ag_name] = res.resource_name
            print(f"Created AdGroup: {ag_name} (Resource: {res.resource_name})")

        # 3. Create Keywords
        agc_service = client.get_service('AdGroupCriterionService')
        keywords_map = {
            'Testing-Advanced-Workflows': [
                "graphql api testing tool",
                "api testing with database",
                "stripe webhook testing",
                "data driven api testing",
                "end to end api testing",
                "api testing visual flow"
            ],
            'Testing-Security-Auth': [
                "test api with client certificate",
                "mutual tls api testing",
                "test api security online"
            ]
        }
        
        kw_ops = []
        for g, kws in keywords_map.items():
            ag_res = ag_res_map[g]
            for kw_text in kws:
                op = client.get_type("AdGroupCriterionOperation")
                crit = op.create
                crit.ad_group = ag_res
                crit.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                crit.keyword.text = kw_text
                crit.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                kw_ops.append(op)
                
        print("Creating Keywords...")
        kw_resp = agc_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
        print(f"Created {len(kw_resp.results)} keywords.")

        # 4. Create RSAs
        ad_service = client.get_service('AdGroupAdService')
        rsa_ops = []
        
        headlines = [
            "Advanced API Testing Tool", "Test GraphQL & SOAP APIs", "API Testing With Database",
            "Test Stripe Webhooks", "Support mTLS API Testing", "Client Certificate Testing",
            "Data-Driven API Tests", "Visual API Flow Control", "End-to-End API Workflows",
            "Professional API Testing", "Secure API Authentication", "Better Than Postman",
            "Complex API Scenarios", "Automated API Testing", "Try Apidog for Free Today"
        ]
        
        descriptions = [
            "Handle complex API scenarios with ease. Support mTLS, visual flow control & databases.",
            "Build data-driven tests in a visual interface. Stop writing boilerplate scripts manually.",
            "The best tool for testing secure APIs requiring mutual TLS and client certificates.",
            "Validate Webhooks, execute database queries & test advanced API logic flawlessly."
        ]
        
        urls_map = {
            'Testing-Advanced-Workflows': "https://apidog.com/api-testing/",
            'Testing-Security-Auth': "https://apidog.com/blog/how-to-test-apis-that-require-client-certificates/"
        }
        
        for g, ag_res in ag_res_map.items():
            op = client.get_type("AdGroupAdOperation")
            ad_group_ad = op.create
            ad_group_ad.ad_group = ag_res
            ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
            ad_group_ad.ad.final_urls.append(urls_map[g])
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
