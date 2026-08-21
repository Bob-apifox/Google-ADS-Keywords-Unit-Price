import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def main():
    try:
        client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
        ga_service = client.get_service("GoogleAdsService")
        
        # Querying change events for the last 2 weeks related to Campaign Criterion (Locations)
        query = """
            SELECT 
              change_event.change_date_time, 
              change_event.campaign, 
              change_event.user_email,
              change_event.resource_change_operation,
              change_event.change_resource_type,
              campaign.name
            FROM change_event 
            WHERE change_event.change_date_time >= '2026-06-29 00:00:00' 
              AND change_event.change_date_time <= '2026-07-13 23:59:59'
              AND change_event.change_resource_type = 'CAMPAIGN_CRITERION'
            ORDER BY change_event.change_date_time DESC
            LIMIT 50
        """
        
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        
        print("--- RECENT CAMPAIGN CRITERION CHANGES ---")
        count = 0
        for batch in stream:
            for row in batch.results:
                event = row.change_event
                # Location criteria usually indicate country settings
                print(f"[{event.change_date_time}] Campaign: {row.campaign.name} | User: {event.user_email} | Operation: {event.resource_change_operation.name}")
                count += 1
        
        if count == 0:
            print("No campaign criterion changes found in the specified date range.")
            
    except Exception as e:
        print(f"Error fetching change history: {e}")

if __name__ == '__main__':
    main()
