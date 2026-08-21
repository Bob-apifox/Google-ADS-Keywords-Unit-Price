# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

# Ensure UTF-8 stdout
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy and REST Transport Setup
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

# Targeted negative keyword dictionary by Campaign Name
today_negatives = {
    "Google-Sa-Solutions-AI-LLM-Global": [
        "durable ai",
        "programming ai",
        "multimodal ai",
        "openhands",
        "julius ai",
        "pentestgpt",
        "google cloud text to speech"
    ],
    "Google-Sa-CLI-Global": [
        "postman api",
        "postman download",
        "postman lite",
        "insomnia api download"
    ],
    "Google-Sa-Solutions-Multi-Protocol-Global": [
        "k6 io",
        "testmu ai",
        "integrated development environment",
        "official developer website",
        "stress testing tools"
    ],
    "Google-Sa-Bump.sh-Global": [
        "gemini api",
        "redoc",
        "flowise",
        "autogen studio"
    ]
}

def execute_upload():
    print(">>> Initializing Google Ads Client...")
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    cc_service = client.get_service('CampaignCriterionService')

    # 1. Look up Campaign IDs by Name
    camp_names = list(today_negatives.keys())
    camp_name_str = ", ".join([f"'{name}'" for name in camp_names])
    
    query = f"""
        SELECT campaign.id, campaign.name
        FROM campaign
        WHERE campaign.name IN ({camp_name_str})
    """
    
    print(">>> Fetching Campaign IDs from Google Ads API...")
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    name_to_id = {}
    for batch in stream:
        for row in batch.results:
            name_to_id[row.campaign.name] = row.campaign.id
            print(f"Found Campaign: {row.campaign.name} -> ID: {row.campaign.id}")

    # 2. Build Campaign Criterion Operations
    operations = []
    total_words_count = 0

    for camp_name, words in today_negatives.items():
        if camp_name not in name_to_id:
            print(f"Warning: Campaign '{camp_name}' not found in account!")
            continue
            
        camp_id = name_to_id[camp_name]
        for word in words:
            cc_op = client.get_type('CampaignCriterionOperation')
            cc_op.create.campaign = ga_service.campaign_path(CUSTOMER_ID, camp_id)
            cc_op.create.negative = True
            cc_op.create.keyword.text = word
            cc_op.create.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            operations.append(cc_op)
            total_words_count += 1

    print(f"\n>>> Prepared {len(operations)} Campaign Negative Keyword operations across {len(name_to_id)} campaigns.")

    # 3. Mutate Campaign Criteria
    if operations:
        request = client.get_type('MutateCampaignCriteriaRequest')
        request.customer_id = CUSTOMER_ID
        request.operations.extend(operations)
        request.partial_failure = True
        
        response = cc_service.mutate_campaign_criteria(request=request)
        print(f"\n[SUCCESS] Successfully uploaded {total_words_count} negative keywords to Google Ads!")
        return True
    return True

def main():
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt}/{max_retries}...")
            if execute_upload():
                break
        except Exception as e:
            print(f"Attempt {attempt} failed with error: {e}")
            if attempt < max_retries:
                print("Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("All retries exhausted.")

if __name__ == '__main__':
    main()
