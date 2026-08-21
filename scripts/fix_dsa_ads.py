import os
from google.ads.googleads.client import GoogleAdsClient

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ['GOOGLE_ADS_USE_REST'] = 'true'

client = GoogleAdsClient.load_from_storage(r"d:\Apidog Work\Google ADS Keywords Unit Price\common\config\google-ads.yaml")
customer_id = "9496728294"

ad_group_ad_service = client.get_service("AdGroupAdService")

competitors = [
    {"name": "Postman", "desc": "Tired of Postman pricing? Switch to Apidog for free team collaboration."},
    {"name": "Insomnia", "desc": "Looking for an Insomnia alternative? Import your data to Apidog in 1 click."},
    {"name": "SwaggerHub", "desc": "Design APIs faster. Switch from SwaggerHub to Apidog for a modern experience."},
    {"name": "ReadMe", "desc": "Better API documentation without the cost. The best ReadMe alternative."},
    {"name": "ReadyAPI", "desc": "Heavy desktop tools slowing you down? Switch from ReadyAPI to Apidog."},
    {"name": "SoapUI", "desc": "Modernize your API testing. Move away from SoapUI to a faster platform."},
    {"name": "Mintlify", "desc": "Auto-generate beautiful API docs. The ultimate Mintlify alternative."},
    {"name": "Bruno", "desc": "Need a powerful API client? Apidog is the perfect alternative to Bruno."},
    {"name": "Hoppscotch", "desc": "Need better team management? Switch from Hoppscotch to Apidog today."}
]

# Find the ad group resources
for comp in competitors:
    query = f"SELECT ad_group.id, ad_group.resource_name FROM ad_group WHERE campaign.name = 'Google-Sa-DSA-Alternatives-Global' AND ad_group.name = 'DSA-{comp['name']}-Alternative'"
    resp = client.get_service("GoogleAdsService").search(customer_id=customer_id, query=query)
    for row in resp:
        ag_resource = row.ad_group.resource_name
        
        ad_op = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_op.create
        ad_group_ad.ad_group = ag_resource
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        ad = ad_group_ad.ad
        ad.expanded_dynamic_search_ad.description = comp['desc']
        ad.expanded_dynamic_search_ad.description2 = "Sign up for free and start testing APIs instantly. Import in seconds."
        
        try:
            ad_group_ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[ad_op])
            print(f"Created Expanded DSA ad for {comp['name']}")
        except Exception as e:
            print(f"Failed {comp['name']}: {e}")
