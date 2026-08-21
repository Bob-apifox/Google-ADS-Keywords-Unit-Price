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
        
        target_campaigns = [
            'Google-Sa-Comp-VSCode-Global',
            'Google-Sa-Solutions-AI-LLM-Global',
            'Google-Sa-MCP-Infrastructure',
            'Google-Sa-Func-MultiProtocol-Global',
            'Google-Sa-Solutions-Multi-Protocol-Global',
            'Google-Sa-Postman-Global',
            'Google-Sa-Insomnia-Global'
        ]
        
        names_str = "', '".join(target_campaigns)
        
        query = f"""
            SELECT campaign.id, campaign.name 
            FROM campaign 
            WHERE campaign.name IN ('{names_str}')
        """
        
        stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
        
        for batch in stream:
            for row in batch.results:
                print(f"Name: {row.campaign.name} | ID: {row.campaign.id}")
                
    except Exception as e:
        print(f"Error fetching campaign IDs: {e}")

if __name__ == '__main__':
    main()
