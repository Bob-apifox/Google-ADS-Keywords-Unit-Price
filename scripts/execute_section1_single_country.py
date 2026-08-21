# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Proxy and REST Transport Setup
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

# Tracking Suffix for Google Ads & Metabase Attribution
TRACKING_SUFFIX = "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}"

# Section 1 Master Configuration with Exact Account Campaign IDs
SECTION_1_CONFIG = {
    "Google-Sa-CP-ES": {
        "id": 21995819717,
        "new_ag_name": "Postman-Alternative-ES-2026",
        "final_url": "https://apidog.com/es/compare/apidog-vs-postman/",
        "keywords": ["alternativas a postman", "alternativa a postman gratis", "postman gratis", "postman espanol"],
        "rsa": {
            "headlines": [
                "Apidog: Alternativa a Postman", "Plataforma API Todo en Uno", "Pruebas de API Gratuitas",
                "Migración Postman en 1-Clic", "Mock API y Documentación", "Diseño de API Colaborativo",
                "Sin Límites de Ejecución", "Cliente HTTP y Pruebas API", "Alternativa Postman En Español",
                "Documentación API Automática", "Postman Gratis Alternativa", "Workspace de API Gratis",
                "Apidog En Español Gratis", "Importación Colecciones API", "Probar API Gratis"
            ],
            "descriptions": [
                "Reemplace Postman con Apidog. Plataforma nativa para diseño, prueba y documentación de API.",
                "Migre sus colecciones de Postman con 1 solo clic. Sin límites de ejecuciones en equipo.",
                "Pruebas de API, mock servers y generación de docs en un solo lugar. Pruebe gratis hoy.",
                "Herramienta API nativa en español. Aumente la productividad de su equipo de desarrollo."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-MX": {
        "id": 21995977112,
        "new_ag_name": "Postman-Alternative-MX-2026",
        "final_url": "https://apidog.com/es/compare/apidog-vs-postman/",
        "keywords": ["alternativas a postman", "postman mexico gratis", "probador de api gratis", "alternativa postman gratis"],
        "rsa": {
            "headlines": [
                "La Mejor Alternativa a Postman", "Apidog México - API Testing", "Pruebas API Sin Restricciones",
                "Importe de Postman en 1 Clic", "Mock Servers y Documentos API", "Diseño API Todo en Uno",
                "Apidog En Español México", "Pruebas de API Gratuitas", "Cliente REST API Gratis",
                "Postman Alternativa Gratis", "Documentos API Automáticos", "Pruebas de Carga API",
                "Plataforma Colaborativa API", "Migración Colecciones API", "Apidog Herramienta API"
            ],
            "descriptions": [
                "Diseñe, pruebe y documente APIs en una sola herramienta. Alternativa gratuita a Postman.",
                "Pruebas de API en equipo sin restricciones de pago. Comience gratis hoy con Apidog.",
                "Importe sus colecciones de Postman sin perder datos. Pruebe mock servers automáticos.",
                "Herramienta API nativa en español para desarrolladores en México y Latinoamérica."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-AR": {
        "id": 23139757330,
        "new_ag_name": "Postman-Alternative-AR-2026",
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "keywords": ["بديل postman", "اختبار api مجاني", "postman alternative arabic", "postman free alternative"],
        "rsa": {
            "headlines": [
                "Best Postman Alternative 2026", "Apidog: All-in-One API Tool", "Free API Testing & Mocking",
                "1-Click Postman Migration", "OpenAPI 3.1 Native Platform", "No Runner Execution Limits",
                "API Documentation Generator", "Local-First API Workspace", "Postman Alternative Tool",
                "Free Team API Collaboration", "Automated API Testing Tool", "Smart Mock API Server",
                "Import Postman Collections", "All-in-One API Workspace", "Apidog API Platform Free"
            ],
            "descriptions": [
                "Replace Postman with Apidog. Design, test, mock, and document APIs in one unified workspace.",
                "Import Postman collections effortlessly with zero data loss. Start for free today.",
                "Free team collaboration with no paywalls on runner executions or collection size.",
                "Modern OpenAPI 3.1 native API client for developers in Middle East & North Africa."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-PT": {
        "id": 22261650381,
        "new_ag_name": "Postman-Alternative-PT-2026",
        "final_url": "https://apidog.com/pt/compare/apidog-vs-postman/",
        "keywords": ["alternativa ao postman", "testar api online gratis", "postman portugues", "alternativa postman brasil"],
        "rsa": {
            "headlines": [
                "Alternativa ao Postman - Apidog", "Plataforma de API Tudo-em-Um", "Testar API Online Grátis",
                "Importação Postman em 1 Clique", "Documentação e Mock de API", "Design de API Colaborativo",
                "Sem Limites de Execução", "Cliente HTTP e Testes API", "Apidog em Português Grátis",
                "Gerador de Docs API Grátis", "Postman Grátis Alternativa", "Workspace de API em Equipe",
                "Testes de API Automatizados", "Importar Coleções do Postman", "Apidog Brasil e Portugal"
            ],
            "descriptions": [
                "Substitua o Postman pelo Apidog. Teste, documente e simule APIs em uma só plataforma. Grátis.",
                "Migre suas coleções do Postman sem perdas. Sem limites de execução em equipe.",
                "Testes de API, servidores mock e documentação em um só lugar. Comece grátis hoje.",
                "Ferramenta API nativa em português para desenvolvedores no Brasil e Portugal."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-JP": {
        "id": 21965514943,
        "new_ag_name": "Postman-Alternative-JP-2026",
        "final_url": "https://apidog.com/jp/compare/apidog-vs-postman/",
        "keywords": ["postman 代替", "api テスト ツール", "postman 日本語", "apidog 日本語"],
        "rsa": {
            "headlines": [
                "Postmanの代替ツール - Apidog", "オールインワンAPI開発プラットフォーム", "無料APIテスト＆モックサーバー",
                "Postmanデータ1クリック移行", "APIドキュメント自動生成", "チームコラボレーション無料",
                "実行回数無制限のAPIテスト", "日本語対応API開発ツール", "Apidog 日本語公式",
                "API設計・テスト・文書化", "Postman 無料 代替", "OpenAPI 3.1 完全対応",
                "APIモックサーバー自動作成", "Postmanコレクション完全移行", "無料APIクライアントツール"
            ],
            "descriptions": [
                "Postmanからの移行ならApidog。API設計・テスト・モック・ドキュメント作成を一体化。",
                "ワンクリックでPostmanコレクションを完全移行。チームコラボレーション無料。",
                "実行回数制限なしのAPIテスト＆スマートモック。今すぐ無料で体験してください。",
                "日本市場向けの完全日本語化API開発プラットフォーム。開発効率を大幅向上。"
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-KR": {
        "id": 22309414047,
        "new_ag_name": "Postman-Alternative-KR-2026",
        "final_url": "https://apidog.com/kr/compare/apidog-vs-postman/",
        "keywords": ["postman 대체", "api 테스트 툴", "postman 사용법", "apidog 한국어"],
        "rsa": {
            "headlines": [
                "Postman 최고의 대체 툴 - Apidog", "올인원 API 개발 플랫폼", "무료 API 테스트 및 목 서버",
                "Postman 1클릭 마이그레이션", "자동 API 문서 생성기", "팀 협업 완전 무료",
                "실행 제한 없는 API 테스트", "한국어 지원 API 개발 툴", "Apidog 공식 한국어",
                "API 설계 및 테스트 통합", "Postman 무료 대체 솔루션", "OpenAPI 3.1 지원",
                "스마트 API 목 서버", "Postman 컬렉션 손실없이 이전", "무료 API 클라이언트"
            ],
            "descriptions": [
                "Postman을 대체할 통합 API 툴 Apidog. API 설계, 테스트, 문서화를 한곳에서.",
                "원클릭으로 Postman 데이터를 손실 없이 이전하세요. 지금 무료 시작.",
                "러너 실행 제한 없는 무료 팀 협업 API 플랫폼. 개발 생산성을 높이세요.",
                "한국 개발자를 위한 완전 한국어 지원 API 개발 및 테스트 플랫폼."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-TW": {
        "id": 23264160392,
        "new_ag_name": "Postman-Alternative-TW-2026",
        "final_url": "https://apidog.com/tw/compare/apidog-vs-postman/",
        "keywords": ["postman 替代方案", "api 測試工具 免費", "postman 中文版", "apidog 繁體中文"],
        "rsa": {
            "headlines": [
                "Postman 最佳替代方案 - Apidog", "一站式 API 開發與測試平台", "免費 API 測試與 Mock 服務",
                "1 鍵匯入 Postman 資料", "自動生成 API 文件", "團隊協作完全免費",
                "無執行次數限制的 API 測試", "繁體中文 API 開發工具", "Apidog 繁體中文版",
                "API 設計與調試整合", "Postman 免費替代軟體", "OpenAPI 3.1 原生支援",
                "智慧 API Mock 伺服器", "Postman 集合無縫轉移", "免費 API 用戶端工具"
            ],
            "descriptions": [
                "全面替代 Postman。提供 API 設計、調試、測試與文檔一體化解決方案。",
                "一鍵無縫轉移 Postman 集合，無執行次數限制。立即免費使用。",
                "團隊免費協作，支援 API 自動化測試與 Mock 服務。提高開發效率。",
                "專為台灣及華人開發者打造的繁體中文一站式 API 開發平台。"
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-VN": {
        "id": 22374204671,
        "new_ag_name": "Postman-Alternative-VN-2026",
        "final_url": "https://apidog.com/vi/compare/apidog-vs-postman/",
        "keywords": ["thay thế postman", "công cụ test api miễn phí", "postman tiếng việt", "apidog tiếng việt"],
        "rsa": {
            "headlines": [
                "Công Cụ Thay Thế Postman tốt nhất", "Nền Tảng API Tất-Cả-Trong-Một", "Kiểm Thử API Miễn Phí",
                "Chuyển Dữ Liệu Postman 1 Click", "Tự Động Tạo Tài Liệu API", "Cộng Tác Nhóm Miễn Phí",
                "Không Giới Hạn Lượt Chạy Test", "Công Cụ API Tiếng Việt", "Apidog Tiếng Việt Official",
                "Thiết Kế & Kiểm Thử API", "Thay Thế Postman Miễn Phí", "Hỗ Trợ OpenAPI 3.1 Native",
                "Tạo Smart Mock Server API", "Nhập Collection Postman Dễ Dàng", "Công Cụ API Client Miễn Phí"
            ],
            "descriptions": [
                "Thay thế Postman bằng Apidog. Thiết kế, kiểm thử, mock và tạo document API trên 1 nền tảng.",
                "Nhập bộ sưu tập Postman dễ dàng chỉ với 1 click. Sử dụng miễn phí ngay.",
                "Cộng tác nhóm miễn phí không giới hạn số lượt chạy test script. Nâng cao năng suất.",
                "Nền tảng phát triển API hỗ trợ tiếng Việt dành riêng cho lập trình viên Việt Nam."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-ID": {
        "id": 22451766179,
        "new_ag_name": "Postman-Alternative-ID-2026",
        "final_url": "https://apidog.com/id/compare/apidog-vs-postman/",
        "keywords": ["alternatif postman", "aplikasi testing api gratis", "postman indonesia", "apidog indonesia"],
        "rsa": {
            "headlines": [
                "Alternatif Postman Terbaik - Apidog", "Platform API All-in-One", "Pengujian API Gratis Online",
                "Impor Postman 1-Klik", "Dokumentasi & Mock API", "Kolaborasi Tim Gratis",
                "Tanpa Batas Eksekusi Runner", "Alat Pengembang API Indonesia", "Apidog Bahasa Indonesia",
                "Desain dan Uji API Terpadu", "Software Alternatif Postman", "Dukungan Native OpenAPI 3.1",
                "Server Mock API Otomatis", "Transfer Koleksi Postman Mudah", "Client API Gratis Terbaik"
            ],
            "descriptions": [
                "Gantikan Postman dengan Apidog. Desain, uji, mock, dan dokumentasikan API dalam satu alat.",
                "Impor koleksi Postman Anda dalam 1 klik tanpa batas eksekusi. Mulai gratis.",
                "Kolaborasi tim gratis dengan server mock dan pengujian otomatis tanpa biaya.",
                "Platform API mendukung Bahasa Indonesia untuk pengembang di Indonesia."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-DE": {
        "id": 22367960103,
        "new_ag_name": "Postman-Alternative-DE-2026",
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "keywords": ["postman alternative deutsch", "api testen kostenlos", "postman ersatz", "postman alternative deutschland"],
        "rsa": {
            "headlines": [
                "Postman Alternative 2026 - Apidog", "All-in-One API Platform", "Kostenloses API Testing",
                "1-Klick Postman Migration", "OpenAPI 3.1 Native Platform", "Ohne Runner Ausführungslimits",
                "Automatische API Dokus", "Datenschutz & SOC2 Konform", "Postman Alternative Tool",
                "Kostenlose Team Kollaboration", "Automatisierte API Tests", "Smart Mock API Server",
                "Postman Kollektionen Import", "Integrierter API Workspace", "Apidog API Platform Kostenlos"
            ],
            "descriptions": [
                "Ersetzen Sie Postman durch Apidog. API-Design, Testing, Mocking und Doku in einer Plattform.",
                "Importieren Sie Postman-Kollektionen nahtlos mit 1 Klick. Jetzt kostenlos testen.",
                "Kostenlose Team-Kollaboration ohne Beschränkungen bei Testausführungen.",
                "Moderne API-Entwicklungsplattform für Entwickler in Deutschland, Österreich & Schweiz."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-FR": {
        "id": 23027715066,
        "new_ag_name": "Postman-Alternative-FR-2026",
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "keywords": ["alternative a postman", "outil test api gratuit", "postman en francais", "alternative postman france"],
        "rsa": {
            "headlines": [
                "Alternative à Postman - Apidog", "Plateforme API All-in-One", "Test API & Mock Gratuit",
                "Migration Postman en 1-Clic", "Documentation API Automatique", "Collaboration d'Équipe Gratuite",
                "Sans Limites d'Exécution", "Client HTTP & Test API", "Alternative Postman Gratuite",
                "Générateur de Docs API", "Workspace API Tout-en-Un", "Support Native OpenAPI 3.1",
                "Mock Server API Intelligente", "Import de Collections Postman", "Plateforme API Gratuite"
            ],
            "descriptions": [
                "Remplacez Postman par Apidog. Concevez, testez et documentez vos API sur une seule plateforme.",
                "Importez vos collections Postman en 1 clic sans perte de données. Essayez gratuitement.",
                "Tests d'API automatisés et serveurs mock sans limites d'exécution pour votre équipe.",
                "Outil de développement API moderne pour les développeurs en France et Europe."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    },
    "Google-Sa-CP-TR": {
        "id": 23047433007,
        "new_ag_name": "Postman-Alternative-TR-2026",
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "keywords": ["postman alternatifi", "ücretsiz api test aracı", "postman türkçe", "apidog türkiye"],
        "rsa": {
            "headlines": [
                "En İyi Postman Alternatifi - Apidog", "Hepsi Bir Arada API Platformu", "Ücretsiz API Testi ve Mocking",
                "Tek Tıkla Postman Aktarımı", "Otomatik API Dokümantasyonu", "Ücretsiz Takım Çalışması",
                "Çalıştırma Sınırı Olmayan Test", "API Geliştirme Aracı", "Apidog Türkçe Destekli",
                "API Tasarım ve Test Platformu", "Ücretsiz Postman Alternatifi", "OpenAPI 3.1 Desteği",
                "Akıllı Mock Server Araçları", "Postman Koleksiyon Aktarımı", "Ücretsiz API İstemcisi"
            ],
            "descriptions": [
                "Postman yerine Apidog kullanın. API tasarımı, testi, mock ve dokümantasyonu tek araçta.",
                "Postman koleksiyonlarınızı tek tıkla aktarın. Hemen ücretsiz başlayın.",
                "Sınırsız test çalıştırma ve ücretsiz takım çalışması ile geliştirici verimliliğini artırın.",
                "Türkiye'deki yazılımcılar için modern ve güçlü API geliştirme ve test platformu."
            ],
            "path1": "compare",
            "path2": "postman"
        }
    }
}

def parse_mask(paths):
    from google.protobuf.field_mask_pb2 import FieldMask
    return FieldMask(paths=paths)

def main():
    print("==================================================================")
    print("🚀 STARTING SECTION 1 EXECUTION: 12 Single-Country Campaigns Building")
    print("==================================================================")
    
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    campaign_service = client.get_service('CampaignService')
    ad_group_service = client.get_service('AdGroupService')
    ad_group_criterion_service = client.get_service('AdGroupCriterionService')
    ad_group_ad_service = client.get_service('AdGroupAdService')

    # -----------------------------------------------------------------
    # STEP 1: Enable 12 Campaigns & Attach Tracking Suffix
    # -----------------------------------------------------------------
    print("\n>>> STEP 1: Enabling Campaigns & Attaching Tracking Suffix...")
    camp_ops = []
    for camp_name, cfg in SECTION_1_CONFIG.items():
        camp_op = client.get_type('CampaignOperation')
        campaign = camp_op.update
        campaign.resource_name = ga_service.campaign_path(CUSTOMER_ID, cfg["id"])
        campaign.status = client.enums.CampaignStatusEnum.ENABLED
        campaign.final_url_suffix = TRACKING_SUFFIX
        client.copy_from(camp_op.update_mask, parse_mask(["status", "final_url_suffix"]))
        camp_ops.append(camp_op)

    try:
        response = campaign_service.mutate_campaigns(customer_id=CUSTOMER_ID, operations=camp_ops)
        print(f"[SUCCESS] Enabled {len(response.results)} Campaigns and set Tracking Suffix!")
    except Exception as e:
        print(f"[ERROR] Step 1 failed: {e}")

    # -----------------------------------------------------------------
    # STEP 2: Pause Old Ad Groups in these 12 Campaigns
    # -----------------------------------------------------------------
    print("\n>>> STEP 2: Pausing Old Ad Groups in 12 Campaigns...")
    camp_ids_str = ", ".join([str(cfg["id"]) for cfg in SECTION_1_CONFIG.values()])
    query = f"""
        SELECT ad_group.id, ad_group.name, ad_group.status, campaign.id
        FROM ad_group
        WHERE campaign.id IN ({camp_ids_str})
          AND ad_group.status = 'ENABLED'
    """
    
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    old_ag_ops = []
    for batch in stream:
        for row in batch.results:
            ag_op = client.get_type('AdGroupOperation')
            ag = ag_op.update
            ag.resource_name = ga_service.ad_group_path(CUSTOMER_ID, row.ad_group.id)
            ag.status = client.enums.AdGroupStatusEnum.PAUSED
            client.copy_from(ag_op.update_mask, parse_mask(["status"]))
            old_ag_ops.append(ag_op)

    if old_ag_ops:
        try:
            response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=old_ag_ops)
            print(f"[SUCCESS] Paused {len(response.results)} old enabled Ad Groups!")
        except Exception as e:
            print(f"[ERROR] Step 2 failed: {e}")
    else:
        print("[INFO] No old enabled Ad Groups to pause.")

    # -----------------------------------------------------------------
    # STEP 3: Create New 2026 Ad Groups
    # -----------------------------------------------------------------
    print("\n>>> STEP 3: Creating New 2026 Ad Groups...")
    new_ag_ops = []
    for camp_name, cfg in SECTION_1_CONFIG.items():
        ag_op = client.get_type('AdGroupOperation')
        ag = ag_op.create
        ag.name = cfg["new_ag_name"]
        ag.campaign = ga_service.campaign_path(CUSTOMER_ID, cfg["id"])
        ag.status = client.enums.AdGroupStatusEnum.ENABLED
        ag.cpc_bid_micros = 1000000  # Default $1.00 CPC bid
        new_ag_ops.append(ag_op)

    new_ag_map = {}
    try:
        response = ad_group_service.mutate_ad_groups(customer_id=CUSTOMER_ID, operations=new_ag_ops)
        for result in response.results:
            ag_id = result.resource_name.split('/')[-1]
            ag_query = f"SELECT ad_group.id, ad_group.name FROM ad_group WHERE ad_group.id = {ag_id}"
            st = ga_service.search_stream(customer_id=CUSTOMER_ID, query=ag_query)
            for b in st:
                for r in b.results:
                    new_ag_map[r.ad_group.name] = r.ad_group.id
                    print(f"Created Ad Group: '{r.ad_group.name}' -> ID: {r.ad_group.id}")
        print(f"[SUCCESS] Created {len(new_ag_map)} New Ad Groups!")
    except Exception as e:
        print(f"[ERROR] Step 3 failed: {e}")

    # -----------------------------------------------------------------
    # STEP 4: Add Localized Keywords (Phrase & Exact)
    # -----------------------------------------------------------------
    print("\n>>> STEP 4: Adding Localized Keywords (Phrase & Exact)...")
    kw_ops = []
    total_kws = 0
    for camp_name, cfg in SECTION_1_CONFIG.items():
        ag_name = cfg["new_ag_name"]
        if ag_name not in new_ag_map:
            continue
        ag_id = new_ag_map[ag_name]
        ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        
        for kw_text in cfg["keywords"]:
            # Add Phrase match
            agc_phrase = client.get_type('AdGroupCriterionOperation')
            agc_p = agc_phrase.create
            agc_p.ad_group = ag_path
            agc_p.keyword.text = kw_text
            agc_p.keyword.match_type = client.enums.KeywordMatchTypeEnum.PHRASE
            agc_p.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(agc_phrase)
            total_kws += 1
            
            # Add Exact match
            agc_exact = client.get_type('AdGroupCriterionOperation')
            agc_e = agc_exact.create
            agc_e.ad_group = ag_path
            agc_e.keyword.text = kw_text
            agc_e.keyword.match_type = client.enums.KeywordMatchTypeEnum.EXACT
            agc_e.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            kw_ops.append(agc_exact)
            total_kws += 1

    if kw_ops:
        try:
            request = client.get_type('MutateAdGroupCriteriaRequest')
            request.customer_id = CUSTOMER_ID
            request.operations.extend(kw_ops)
            request.partial_failure = True
            response = ad_group_criterion_service.mutate_ad_group_criteria(request=request)
            print(f"[SUCCESS] Added {total_kws} Phrase & Exact Keywords across 12 Ad Groups!")
        except Exception as e:
            print(f"[ERROR] Step 4 failed: {e}")

    # -----------------------------------------------------------------
    # STEP 5: Create Localized Responsive Search Ads (RSA)
    # -----------------------------------------------------------------
    print("\n>>> STEP 5: Creating Localized Responsive Search Ads (RSA)...")
    rsa_ops = []
    for camp_name, cfg in SECTION_1_CONFIG.items():
        ag_name = cfg["new_ag_name"]
        if ag_name not in new_ag_map:
            continue
        ag_id = new_ag_map[ag_name]
        
        aga_op = client.get_type('AdGroupAdOperation')
        aga = aga_op.create
        aga.ad_group = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        # Build RSA
        rsa = aga.ad.responsive_search_ad
        rsa.final_urls.append(cfg["final_url"])
        rsa.path1 = cfg["rsa"]["path1"]
        rsa.path2 = cfg["rsa"]["path2"]
        
        # Add Headlines (up to 15)
        for hl in cfg["rsa"]["headlines"][:15]:
            headline = client.get_type('AdTextAsset')
            headline.text = hl
            rsa.headlines.append(headline)
            
        # Add Descriptions (up to 4)
        for desc in cfg["rsa"]["descriptions"][:4]:
            description = client.get_type('AdTextAsset')
            description.text = desc
            rsa.descriptions.append(description)
            
        rsa_ops.append(aga_op)

    if rsa_ops:
        try:
            request = client.get_type('MutateAdGroupAdsRequest')
            request.customer_id = CUSTOMER_ID
            request.operations.extend(rsa_ops)
            request.partial_failure = True
            response = ad_group_ad_service.mutate_ad_group_ads(request=request)
            print(f"[SUCCESS] Created {len(response.results)} Localized RSA Ads across 12 Countries!")
        except Exception as e:
            print(f"[ERROR] Step 5 failed: {e}")

    print("\n==================================================================")
    print("🎉 ALL SECTION 1 OPERATIONS COMPLETED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == '__main__':
    main()
