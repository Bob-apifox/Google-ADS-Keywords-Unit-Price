import os
from google.ads.googleads.client import GoogleAdsClient
from google.api_core import protobuf_helpers

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

GOOGLE_ADS_YAML = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'
CUSTOMER_ID = '9496728294'

client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
campaign_service = client.get_service('CampaignService')
campaign_criterion_service = client.get_service('CampaignCriterionService')
ad_group_service = client.get_service('AdGroupService')
ad_group_criterion_service = client.get_service('AdGroupCriterionService')
ad_group_ad_service = client.get_service('AdGroupAdService')

campaigns_data = {
    '23981394894': {
        'negative_keywords': ['tutorial', 'how to install', 'not working', 'source code', 'github repository', 'crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'Thunder-Client': {
                'cpc_bid': 1.50,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'thunder client', 'match': 'EXACT'},
                    {'text': 'thunder client', 'match': 'PHRASE'},
                    {'text': 'thunder client alternative', 'match': 'EXACT'},
                    {'text': 'thunder client alternative', 'match': 'PHRASE'},
                    {'text': 'thunder client vs postman', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Switch from Thunder Client", "Best API Design Platform", "Thunder Client Alternative", "Upgrade Your API Workflow", "Apidog vs Thunder Client"],
                    'descriptions': ["Upgrade from simple extensions. Get a unified workspace for API Design and Mocking.", "Experience seamless API testing and team collaboration in one platform.", "Join 1,000,000+ developers using Apidog for a faster workflow."],
                }]
            },
            'REST-Client': {
                'cpc_bid': 1.50,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'rest client vscode', 'match': 'EXACT'},
                    {'text': 'rest client vscode', 'match': 'PHRASE'},
                    {'text': 'huachao mao rest client', 'match': 'EXACT'},
                    {'text': 'vscode api client', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["VS Code REST Client Alternative", "Better API Client", "Switch to Apidog Today", "Advanced API Testing Tool", "Free API Client"],
                    'descriptions': ["Upgrade from simple extensions. Get a unified workspace for API Design and Mocking.", "Stop struggling with simple extensions. Import data in 1 click and automate tests.", "Join 1,000,000+ developers using Apidog for a faster workflow."],
                }]
            },
            'RapidAPI-Ext': {
                'cpc_bid': 1.50,
                'final_url': 'https://apidog.com/compare/apidog-vs-rapidapi',
                'keywords': [
                    {'text': 'rapidapi vscode', 'match': 'PHRASE'},
                    {'text': 'rapidapi extension', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["RapidAPI Extension Alternative", "Better than RapidAPI", "Migrate from RapidAPI", "Advanced API Testing Tool", "Switch to Apidog Today"],
                    'descriptions': ["Upgrade from RapidAPI. Get a unified workspace for API Design and Mocking.", "Stop struggling with simple extensions. Import data in 1 click and automate tests.", "Join 1,000,000+ developers using Apidog for a faster workflow."],
                }]
            }
        }
    },
    '23981398449': {
        'negative_keywords': ['jobs', 'salary', 'career', 'interview questions', 'certification', 'freelance', 'crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'SoapUI': {
                'cpc_bid': 2.50,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'soapui alternative', 'match': 'EXACT'},
                    {'text': 'soapui alternative', 'match': 'PHRASE'},
                    {'text': 'soapui pro alternative', 'match': 'PHRASE'},
                    {'text': 'migrate from soapui', 'match': 'PHRASE'},
                    {'text': 'soapui replacement', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Modern SoapUI Alternative", "Migrate from SoapUI Easily", "Zero Code API Testing", "Better than SoapUI Pro", "Apidog API Testing"],
                    'descriptions': ["Zero-code API Testing automation. Modern, fast, and easier than SoapUI.", "Import from SoapUI in 1-click. Stop writing manual scripts for API testing.", "Visual test cases, CI/CD integration, and automated assertions."],
                }]
            },
            'ReadyAPI': {
                'cpc_bid': 2.50,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'readyapi alternative', 'match': 'EXACT'},
                    {'text': 'readyapi alternative', 'match': 'PHRASE'},
                    {'text': 'readyapi vs', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["ReadyAPI Alternative", "Modern API Testing Tool", "Zero Code API Testing", "Migrate from ReadyAPI", "Apidog API Testing"],
                    'descriptions': ["Zero-code API Testing automation. Modern, fast, and easier than ReadyAPI.", "Import data in 1-click. Stop writing manual scripts for API testing.", "Visual test cases, CI/CD integration, and automated assertions."],
                }]
            },
            'Katalon-Karate': {
                'cpc_bid': 2.50,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'katalon api alternative', 'match': 'PHRASE'},
                    {'text': 'karate dsl alternative', 'match': 'PHRASE'},
                    {'text': 'karate api testing', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Modern API Testing Platform", "Zero Code API Testing", "Katalon Alternative", "Karate DSL Alternative", "Apidog API Testing"],
                    'descriptions': ["Zero-code API Testing automation. Visual test cases and CI/CD integration.", "Stop writing manual scripts. Automate your API testing with ease.", "Visual test cases, CI/CD integration, and automated assertions."],
                }]
            }
        }
    },
    '23990938534': {
        'negative_keywords': ['obsidian', 'notion', 'markdown offline', 'pdf converter', 'crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'Redocly': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'redocly alternative', 'match': 'EXACT'},
                    {'text': 'redocly alternative', 'match': 'PHRASE'},
                    {'text': 'redoc vs', 'match': 'PHRASE'},
                    {'text': 'redoc alternative', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Redocly Alternative", "Generate Interactive API Docs", "Stop Writing Markdown", "Beautiful API Documentation", "Apidog Documentation"],
                    'descriptions': ["Stop writing Markdown for APIs. Auto-generate beautiful, interactive API docs with Apidog.", "Syncs automatically with your code. Includes a built-in API debugger for users.", "Join 1,000,000+ developers generating interactive documentation easily."],
                }]
            },
            'Docusaurus': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'docusaurus api docs', 'match': 'PHRASE'},
                    {'text': 'docusaurus alternative', 'match': 'PHRASE'},
                    {'text': 'slate api docs', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Docusaurus Alternative", "Generate Interactive API Docs", "Stop Writing Markdown", "Beautiful API Documentation", "Apidog Documentation"],
                    'descriptions': ["Stop writing Markdown for APIs. Auto-generate beautiful, interactive API docs with Apidog.", "Syncs automatically with your code. Includes a built-in API debugger for users.", "Join 1,000,000+ developers generating interactive documentation easily."],
                }]
            },
            'Apiary-GitBook': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/',
                'keywords': [
                    {'text': 'apiary alternative', 'match': 'PHRASE'},
                    {'text': 'gitbook api documentation', 'match': 'PHRASE'},
                    {'text': 'gitbook alternative', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Apiary Alternative", "GitBook Alternative for APIs", "Generate Interactive API Docs", "Beautiful API Documentation", "Apidog Documentation"],
                    'descriptions': ["Stop writing Markdown for APIs. Auto-generate beautiful, interactive API docs with Apidog.", "Syncs automatically with your code. Includes a built-in API debugger for users.", "Join 1,000,000+ developers generating interactive documentation easily."],
                }]
            }
        }
    },
    '23986384244': {
        'negative_keywords': ['crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'Contract-Testing': {
                'cpc_bid': 2.50,
                'final_url': 'https://apidog.com/api-testing-tools',
                'keywords': [
                    {'text': 'api contract testing', 'match': 'EXACT'},
                    {'text': 'api contract testing', 'match': 'PHRASE'},
                    {'text': 'consumer driven contracts', 'match': 'PHRASE'},
                    {'text': 'contract testing microservices', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["API Contract Testing", "Microservices Contract Testing", "Automated Contract Checks", "Ensure Backend Consistency", "Apidog Testing Platform"],
                    'descriptions': ["Automated API Contract Testing based on Schema. Ensure frontend-backend consistency.", "Detect breaking changes instantly. Zero-code setup for microservices.", "Join 1,000,000+ developers using Apidog for reliable contract testing."],
                }]
            },
            'Pact-Alternative': {
                'cpc_bid': 2.50,
                'final_url': 'https://apidog.com/api-testing-tools',
                'keywords': [
                    {'text': 'pact testing alternative', 'match': 'EXACT'},
                    {'text': 'pact testing alternative', 'match': 'PHRASE'},
                    {'text': 'pact vs', 'match': 'PHRASE'},
                    {'text': 'pact contract testing', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Pact Testing Alternative", "Better API Contract Testing", "Microservices Contract Checks", "Ensure Backend Consistency", "Apidog Testing Platform"],
                    'descriptions': ["Automated API Contract Testing based on Schema. Ensure frontend-backend consistency.", "Detect breaking changes instantly. Zero-code setup for microservices.", "Join 1,000,000+ developers using Apidog for reliable contract testing."],
                }]
            }
        }
    },
    '23990942638': {
        'negative_keywords': ['crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'API-Pipeline': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/apidog-cli',
                'keywords': [
                    {'text': 'automated api pipeline', 'match': 'EXACT'},
                    {'text': 'automated api pipeline', 'match': 'PHRASE'},
                    {'text': 'api testing in ci cd', 'match': 'PHRASE'},
                    {'text': 'api regression testing', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Automated API Pipeline", "API Testing in CI/CD", "Native CI/CD Integration", "Apidog CLI for Testing", "Automate API Regression"],
                    'descriptions': ["Native CI/CD Integration via Apidog CLI. Automate API testing in Jenkins or GitHub.", "Run your API tests in the pipeline with a single command. Get instant reports.", "Join 1,000,000+ developers using Apidog for automated testing."],
                }]
            },
            'Newman-Integration': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/apidog-cli',
                'keywords': [
                    {'text': 'newman jenkins integration', 'match': 'PHRASE'},
                    {'text': 'api testing jenkins', 'match': 'PHRASE'},
                    {'text': 'api testing github actions', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Newman Alternative", "API Testing in Jenkins", "GitHub Actions API Testing", "Native CI/CD Integration", "Apidog CLI for Testing"],
                    'descriptions': ["Native CI/CD Integration via Apidog CLI. Automate API testing in Jenkins or GitHub.", "Run your API tests in the pipeline with a single command. Get instant reports.", "Join 1,000,000+ developers using Apidog for automated testing."],
                }]
            }
        }
    },
    '23981407167': {
        'negative_keywords': ['crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'GraphQL-gRPC': {
                'cpc_bid': 1.50,
                'final_url': 'https://apidog.com/solutions/multi-protocol-api-development',
                'keywords': [
                    {'text': 'graphql query builder', 'match': 'PHRASE'},
                    {'text': 'graphql testing tool', 'match': 'PHRASE'},
                    {'text': 'grpc testing tool', 'match': 'PHRASE'},
                    {'text': 'grpc client', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["GraphQL Testing Tool", "gRPC Client & Testing", "Test Any Protocol Easily", "Unified API Platform", "Apidog Multi-Protocol"],
                    'descriptions': ["One Unified Platform for REST, GraphQL, WebSocket, and gRPC debugging.", "Stop switching between tools. Design, mock, and test all protocols in Apidog.", "Join 1,000,000+ developers building APIs faster."],
                }]
            },
            'WebSocket-SSE': {
                'cpc_bid': 1.50,
                'final_url': 'https://apidog.com/solutions/multi-protocol-api-development',
                'keywords': [
                    {'text': 'websocket test client', 'match': 'PHRASE'},
                    {'text': 'websocket api testing', 'match': 'PHRASE'},
                    {'text': 'sse debugger', 'match': 'PHRASE'},
                    {'text': 'server sent events test', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["WebSocket Test Client", "SSE Debugging Tool", "Test Real-time APIs", "Unified API Platform", "Apidog Multi-Protocol"],
                    'descriptions': ["One Unified Platform for REST, GraphQL, WebSocket, and gRPC debugging.", "Stop switching between tools. Design, mock, and test all protocols in Apidog.", "Join 1,000,000+ developers building APIs faster."],
                }]
            }
        }
    },
    '23981409303': {
        'negative_keywords': ['crack', 'free premium', 'uninstall', 'error code', 'login'],
        'ad_groups': {
            'Service-Virtualization': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/api-mocking-tools',
                'keywords': [
                    {'text': 'api service virtualization', 'match': 'EXACT'},
                    {'text': 'api service virtualization', 'match': 'PHRASE'},
                    {'text': 'service virtualization tool', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["API Service Virtualization", "Advanced Mock Server", "Dynamic Data Mocking", "Smart API Mock Engine", "Apidog Mock Server"],
                    'descriptions': ["Advanced API Mocking Server. Return dynamic data based on request parameters.", "Generate realistic mock data instantly. No need to write complex mock servers.", "Join 1,000,000+ developers accelerating frontend development."],
                }]
            },
            'Wiremock-Alternative': {
                'cpc_bid': 2.00,
                'final_url': 'https://apidog.com/api-mocking-tools',
                'keywords': [
                    {'text': 'wiremock alternative', 'match': 'EXACT'},
                    {'text': 'wiremock alternative', 'match': 'PHRASE'},
                    {'text': 'wiremock vs', 'match': 'PHRASE'},
                    {'text': 'dynamic api mocking', 'match': 'PHRASE'},
                    {'text': 'mock server script logic', 'match': 'PHRASE'}
                ],
                'ads': [{
                    'headlines': ["Wiremock Alternative", "Advanced Mock Server", "Dynamic Data Mocking", "Smart API Mock Engine", "Apidog Mock Server"],
                    'descriptions': ["Advanced API Mocking Server. Return dynamic data based on request parameters.", "Generate realistic mock data instantly. No need to write complex mock servers.", "Join 1,000,000+ developers accelerating frontend development."],
                }]
            }
        }
    }
}

tracking_url_template = "{lpurl}?utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_content={adgroupid}&utm_term={keyword}"

print("Starting Injection Process...")
for c_id, c_data in campaigns_data.items():
    print(f"\n--- Processing Campaign {c_id} ---")
    
    # 1. Inject Negative Keywords
    neg_ops = []
    for word in c_data['negative_keywords']:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        criterion.negative = True
        criterion.keyword.text = word
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
        neg_ops.append(op)
    
    if neg_ops:
        try:
            campaign_criterion_service.mutate_campaign_criteria(customer_id=CUSTOMER_ID, operations=neg_ops)
            print(f"Added {len(neg_ops)} negative keywords.")
        except Exception as e:
            print(f"Error adding negative keywords: {e}")

    # 2. Inject Ad Groups
    for ag_name, ag_data in c_data['ad_groups'].items():
        ag_op = client.get_type("AdGroupOperation")
        ad_group = ag_op.create
        ad_group.name = ag_name
        ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
        ad_group.campaign = campaign_service.campaign_path(CUSTOMER_ID, c_id)
        ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
        ad_group.cpc_bid_micros = int(ag_data['cpc_bid'] * 1000000)

        try:
            ag_response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=[ag_op])
            ag_resource_name = ag_response.results[0].resource_name
            print(f"  Created Ad Group: {ag_name}")

            # 3. Inject Keywords
            kw_ops = []
            for kw in ag_data['keywords']:
                kw_op = client.get_type("AdGroupCriterionOperation")
                criterion = kw_op.create
                criterion.ad_group = ag_resource_name
                criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
                criterion.keyword.text = kw['text']
                if kw['match'] == 'EXACT':
                    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
                else:
                    criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
                kw_ops.append(kw_op)
            
            try:
                ad_group_criterion_service.mutate_ad_group_criteria(customer_id=CUSTOMER_ID, operations=kw_ops)
                print(f"    Added {len(kw_ops)} keywords.")
            except Exception as e:
                print(f"    Error adding keywords: {e}")

            # 4. Inject Ads (RSA)
            ad_ops = []
            for ad_info in ag_data['ads']:
                ad_op = client.get_type("AdGroupAdOperation")
                ad_group_ad = ad_op.create
                ad_group_ad.ad_group = ag_resource_name
                ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
                
                ad = ad_group_ad.ad
                ad.final_urls.append(ag_data['final_url'])
                ad.tracking_url_template = tracking_url_template
                
                # set RSA
                rsa = ad.responsive_search_ad
                for text in ad_info['headlines']:
                    h = client.get_type("AdTextAsset")
                    h.text = text
                    rsa.headlines.append(h)
                for text in ad_info['descriptions']:
                    d = client.get_type("AdTextAsset")
                    d.text = text
                    rsa.descriptions.append(d)
                    
                ad_ops.append(ad_op)

            try:
                ad_group_ad_service.mutate_ad_group_ads(customer_id=CUSTOMER_ID, operations=ad_ops)
                print(f"    Added {len(ad_ops)} RSA ads.")
            except Exception as e:
                print(f"    Error adding ads: {e}")

        except Exception as e:
            print(f"  Error creating ad group {ag_name}: {e}")

    # 5. Enable Campaign
    camp_op = client.get_type("CampaignOperation")
    camp = camp_op.update
    camp.resource_name = campaign_service.campaign_path(CUSTOMER_ID, c_id)
    camp.status = client.enums.CampaignStatusEnum.ENABLED
    client.copy_from(camp_op.update_mask, protobuf_helpers.field_mask(None, camp._pb))
    
    try:
        campaign_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=[camp_op])
        print(f"Enabled Campaign {c_id}")
    except Exception as e:
        print(f"Error enabling campaign: {e}")

print("\nALL DONE.")
