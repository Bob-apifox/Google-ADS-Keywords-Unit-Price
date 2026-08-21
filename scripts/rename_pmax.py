import os
import sys
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
sys.stdout.reconfigure(encoding='utf-8')

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
asset_group_service = client.get_service('AssetGroupService')
customer_id = '9496728294'

def rename_asset_groups():
    print(">>> Renaming PMax Asset Groups...")
    
    # Global
    op1 = client.get_type('AssetGroupOperation')
    ag1 = op1.update
    ag1.resource_name = asset_group_service.asset_group_path(customer_id, '6560253413')
    ag1.name = 'AssetGroup-Apidog-All-in-One'
    op1.update_mask.paths.append("name")
    
    # Postman
    op2 = client.get_type('AssetGroupOperation')
    ag2 = op2.update
    ag2.resource_name = asset_group_service.asset_group_path(customer_id, '6692218014')
    ag2.name = 'AssetGroup-Postman-Interception'
    op2.update_mask.paths.append("name")
    
    try:
        resp = asset_group_service.mutate_asset_groups(customer_id=customer_id, operations=[op1, op2])
        print(f"Successfully renamed {len(resp.results)} Asset Groups.")
    except Exception as e:
        print(f"Error renaming Asset Groups: {e}")

if __name__ == '__main__':
    rename_asset_groups()
