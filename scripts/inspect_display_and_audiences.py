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

    # 1. Check User Lists (Remarketing Audiences)
    q_userlists = """
        SELECT
            user_list.id,
            user_list.name,
            user_list.type,
            user_list.membership_status,
            user_list.size_for_display,
            user_list.size_for_search
        FROM user_list
        WHERE user_list.membership_status = 'OPEN'
        ORDER BY user_list.size_for_display DESC
        LIMIT 20
    """
    print("=== AVAILABLE USER LISTS (REMARKETING AUDIENCES) ===")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_userlists):
            for row in batch.results:
                ul = row.user_list
                print(f"ID: {ul.id:<15} | Name: {ul.name:<40} | Display Size: {ul.size_for_display:<8} | Search Size: {ul.size_for_search}")
    except Exception as e:
        print(f"Error querying user lists: {e}")

    # 2. Check Existing Display Campaigns
    q_display = """
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type
        FROM campaign
        WHERE campaign.advertising_channel_type = 'DISPLAY'
    """
    print("\n=== EXISTING DISPLAY CAMPAIGNS ===")
    try:
        for batch in ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_display):
            for row in batch.results:
                c = row.campaign
                print(f"ID: {c.id} | Name: {c.name} | Status: {c.status.name}")
    except Exception as e:
        print(f"Error querying display campaigns: {e}")

if __name__ == '__main__':
    main()
