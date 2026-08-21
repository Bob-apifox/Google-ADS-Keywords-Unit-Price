import os
from google.ads.googleads.client import GoogleAdsClient

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

client = GoogleAdsClient.load_from_storage('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
ga_service = client.get_service('GoogleAdsService')
agbc_service = client.get_service('AdGroupCriterionService')

q = "SELECT ad_group.id, ad_group.name FROM ad_group WHERE campaign.name = 'Google-Sa-Postman-Global' AND ad_group.name = 'Postman Alternative-Global'"
stream = ga_service.search_stream(customer_id='9496728294', query=q)
ag_id = None
for batch in stream:
    for row in batch.results:
        ag_id = row.ad_group.id

if ag_id:
    ag_path = ga_service.ad_group_path('9496728294', ag_id)
    op = client.get_type('AdGroupCriterionOperation')
    agc = op.create
    agc.ad_group = ag_path
    agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    agc.keyword.text = "test keyword"
    agc.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
    
    req = client.get_type('MutateAdGroupCriteriaRequest')
    req.customer_id = '9496728294'
    req.operations.append(op)
    req.partial_failure = True
    resp = agbc_service.mutate_ad_group_criteria(request=req)
    print(resp)
