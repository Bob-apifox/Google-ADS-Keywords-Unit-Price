# -*- coding: utf-8 -*-
import os
import json
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

campaign_ids = [22061425619, 22067541248, 22892634645, 22923613652, 23030065589, 
                23320166856, 23347684482, 23376992548, 23716128367, 23770423434, 23921795178]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    
    ids_str = ', '.join(map(str, campaign_ids))
    query = f'''
        SELECT
            campaign.id,
            campaign.name,
            ad_group.id,
            ad_group.name,
            metrics.cost_micros,
            metrics.conversions,
            metrics.clicks
        FROM ad_group
        WHERE segments.date DURING LAST_30_DAYS
          AND campaign.id IN ({ids_str})
          AND ad_group.status = 'ENABLED'
    '''
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    results = []
    
    for batch in stream:
        for row in batch.results:
            cost = row.metrics.cost_micros / 1000000.0 if row.metrics.cost_micros else 0
            conversions = row.metrics.conversions if row.metrics.conversions else 0
            clicks = row.metrics.clicks if row.metrics.clicks else 0
            
            actual_cpa = cost / conversions if conversions > 0 else (float('inf') if cost > 0 else 0)
            
            results.append({
                'campaign_name': row.campaign.name,
                'ad_group_name': row.ad_group.name,
                'ad_group_id': row.ad_group.id,
                'cost': cost,
                'conversions': conversions,
                'actual_cpa': actual_cpa,
                'clicks': clicks
            })
            
    with open('ag_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print('Data saved to ag_analysis.json')

main()

