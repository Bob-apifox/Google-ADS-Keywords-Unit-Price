# -*- coding: utf-8 -*-
import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    query = '''
        SELECT
            campaign.id,
            campaign.name,
            campaign.target_cpa.target_cpa_micros,
            campaign.maximize_conversions.target_cpa_micros
        FROM campaign
        WHERE campaign.status = 'ENABLED'
    '''
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    found_campaigns = []
    
    for batch in stream:
        for row in batch.results:
            try:
                cpa_1 = row.campaign.target_cpa.target_cpa_micros
                cpa_2 = row.campaign.maximize_conversions.target_cpa_micros
                cpa_micros = cpa_1 if cpa_1 else cpa_2
                if cpa_micros:
                    val = cpa_micros / 1000000.0
                    if abs(val - 2.5) < 0.01:
                        found_campaigns.append((row.campaign.name, row.campaign.id))
            except Exception as e:
                pass
                
    if found_campaigns:
        print('Found the following Campaigns with Target CPA = .5:')
        for name, cid in found_campaigns:
            print(f' - {name} (ID: {cid})')
    else:
        print('No campaigns found with exactly .5 Target CPA.')

main()

