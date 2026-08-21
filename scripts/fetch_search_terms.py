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
            campaign.name,
            ad_group.name,
            search_term_view.search_term,
            metrics.cost_micros,
            metrics.conversions,
            metrics.clicks
        FROM search_term_view
        WHERE segments.date DURING LAST_30_DAYS
          AND campaign.id IN ({ids_str})
          AND metrics.cost_micros > 0
        ORDER BY metrics.cost_micros DESC
    '''
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    results = []
    
    for batch in stream:
        for row in batch.results:
            cost = row.metrics.cost_micros / 1000000.0
            conv = row.metrics.conversions
            clicks = row.metrics.clicks
            results.append({
                'campaign': row.campaign.name,
                'ad_group': row.ad_group.name,
                'search_term': row.search_term_view.search_term,
                'cost': cost,
                'conversions': conv,
                'clicks': clicks
            })
            
    with open('search_terms.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f'Saved {len(results)} search terms to search_terms.json')

if __name__ == '__main__':
    main()
