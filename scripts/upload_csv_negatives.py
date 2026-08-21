import os
import sys
import csv
import urllib3

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
campaign_criterion_service = client.get_service('CampaignCriterionService')
customer_id = '9496728294'

csv_path = r"d:\Apidog Work\Google ADS Keywords Unit Price\keyword_unit_price\reports\negative_keywords_2026_08_14.csv"

keywords = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        keywords.append((row['Keyword'], row['Match Type']))

# Get all ENABLED Search campaigns
q = """
    SELECT campaign.id, campaign.name 
    FROM campaign 
    WHERE campaign.status = 'ENABLED' 
    AND campaign.advertising_channel_type = 'SEARCH'
"""
stream = ga_service.search(customer_id=customer_id, query=q)

camp_ids = []
for row in stream:
    camp_ids.append((row.campaign.id, row.campaign.name))

print(f"Found {len(camp_ids)} active search campaigns.")

operations = []
for camp_id, camp_name in camp_ids:
    for kw, match_type in keywords:
        operation = client.get_type("CampaignCriterionOperation")
        criterion = operation.create
        criterion.campaign = ga_service.campaign_path(customer_id, camp_id)
        criterion.negative = True
        criterion.keyword.text = kw
        if match_type.upper() == 'EXACT':
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        else:
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
        
        operations.append(operation)

print(f"Prepared {len(operations)} operations.")

# Chunk operations into groups of 2000
chunk_size = 2000
for i in range(0, len(operations), chunk_size):
    chunk = operations[i:i + chunk_size]
    print(f"Mutating chunk {i//chunk_size + 1}, size {len(chunk)}...")
    try:
        request = client.get_type('MutateCampaignCriteriaRequest')
        request.customer_id = customer_id
        request.operations.extend(chunk)
        request.partial_failure = True
        response = campaign_criterion_service.mutate_campaign_criteria(request=request)
        print(f"Successfully sent chunk request.")
    except Exception as e:
        print(f"Error mutating chunk: {e}")

print("Done!")
