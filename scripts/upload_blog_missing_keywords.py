import os
import sys
import urllib3
from google.ads.googleads.client import GoogleAdsClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
os.environ['grpc_proxy'] = 'http://127.0.0.1:7890'
os.environ["GOOGLE_ADS_USE_REST"] = "true"
sys.stdout.reconfigure(encoding='utf-8')

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

# 31 missing keywords mapped to Campaign & AdGroup names
missing_kw_mappings = [
    ("reqbin alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("kreya alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("testfully alternative", "Google-Sa-DSA-Alternatives-Global", "DSA-Postman-Alternative"),
    ("stoplight openapi alternative", "Google-Sa-Stoplight-Global", "Stoplight Alternative--Global"),
    ("cloud mock server", "Google-Sa-Mock-Global", "Mock-Global"),
    ("self hosted mock server", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("conditional mock api", "Google-Sa-Func-AdvancedMock-Global", "Wiremock-Alternative"),
    ("zero code mock api", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("auto mock api", "Google-Sa-Mock-Global", "Smart-Mock-Server"),
    ("prism mock alternative", "Google-Sa-Func-AdvancedMock-Global", "Wiremock-Alternative"),
    ("soap wsdl api testing", "Google-Sa-Testing-Global", "Testing-Global"),
    ("mtls api testing", "Google-Sa-Testing-Global", "API-Security-Testing"),
    ("client certificate api test", "Google-Sa-Testing-Global", "Testing-Security-Auth"),
    ("test file upload api", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("test stripe webhooks", "Google-Sa-Solutions-Multi-Protocol-Global", "Webhook Testing"),
    ("api test with database assertion", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("conditional api test scenarios", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("import har to api test", "Google-Sa-Testing-Global", "Testing-Advanced-Workflows"),
    ("schedule api automated tests", "Google-Sa-Testing-Global", "Automated-API-Regression-Runner"),
    ("circleci api testing", "Google-Sa-Func-CICD-Global", "API-Pipeline"),
    ("drone ci api testing", "Google-Sa-Func-CICD-Global", "API-Pipeline"),
    ("cli api testing tool", "Google-Sa-CLI-Terminal-Global", "CLI-Automated-Testing"),
    ("api regression testing tool", "Google-Sa-Func-CICD-Global", "Newman-Integration"),
    ("apachebench alternative", "Google-Sa-Jmeter-Global", "JMeter-Replacement-Global"),
    ("ab load testing gui", "Google-Sa-Jmeter-Global", "Jmeter---Global"),
    ("autocannon load testing", "Google-Sa-Jmeter-Global", "API-Performance-Ease-Global"),
    ("artillery api load testing", "Google-Sa-Jmeter-Global", "JMeter-Replacement-Global"),
    ("http api load testing tool", "Google-Sa-Jmeter-Global", "API-Performance-Ease-Global"),
    ("api secret scanner", "Google-Sa-Enterprise-Killer-Global", "API-Testing-Comparison"),
    ("api audit logs tool", "Google-Sa-Enterprise-Killer-Global", "API-Testing-Comparison"),
    ("openapi client code generator", "Google-Sa-Openapi-Global", "Openapi--Global")
]

def main():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service("GoogleAdsService")
    agc_service = client.get_service("AdGroupCriterionService")
    
    # Query Ad Group resource names for target campaigns and ad groups
    query = """
        SELECT
            campaign.name,
            ad_group.id,
            ad_group.name,
            ad_group.resource_name
        FROM ad_group
        WHERE ad_group.status = 'ENABLED'
    """
    
    ag_map = {}
    stream = ga_service.search(customer_id=CUSTOMER_ID, query=query)
    for row in stream:
        cname = row.campaign.name
        agname = row.ad_group.name
        res_name = row.ad_group.resource_name
        ag_map[(cname, agname)] = res_name
        
    ops = []
    for kw, cname, agname in missing_kw_mappings:
        key = (cname, agname)
        if key in ag_map:
            ag_res_name = ag_map[key]
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = ag_res_name
            criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            criterion.keyword.text = kw
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            ops.append((kw, cname, agname, op))
        else:
            print(f"⚠️ Could not find AdGroup resource name for ({cname} > {agname})")

    print(f"Prepared {len(ops)} operations to ADD missing Blog keywords as PHRASE match.")
    
    if ops:
        mutate_ops = [item[3] for item in ops]
        req = client.get_type("MutateAdGroupCriteriaRequest")
        req.customer_id = CUSTOMER_ID
        req.operations.extend(mutate_ops)
        req.partial_failure = True
        
        try:
            res = agc_service.mutate_ad_group_criteria(request=req)
            print(f"✅ Successfully added {len(ops)} missing Blog keywords into existing Ad Groups!")
        except Exception as e:
            print(f"Error mutating criteria: {e}")

if __name__ == '__main__':
    main()
