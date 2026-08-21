# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib3
from google.ads.googleads.client import GoogleAdsClient

try: sys.stdout.reconfigure(encoding='utf-8')
except: pass
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["grpc_proxy"] = "http://127.0.0.1:7890"
os.environ["GOOGLE_ADS_USE_REST"] = "true"

GOOGLE_ADS_YAML = os.path.join('d:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml')
CUSTOMER_ID = '9496728294'

def get_len(text):
    return sum(2 if ord(c) > 127 else 1 for c in text)

def shorten(text, max_len):
    while get_len(text) > max_len:
        text = text[:-1]
    return text.strip()

# Map specific campaigns to the language config we should use for creatives
# This handles the weird naming (TR -> Spanish, FR -> French, ar -> Arabic)
CAMPAIGN_MAPPING = {
    "Google-Sa-CP-TR": {"old_ag": "Postman-ESP", "lang": "ES"},
    "Google-Sa-CP-FR": {"old_ag": "Postman-ESP", "lang": "FR"},
    "Google-Sa-CP-TW": {"old_ag": "Postman-TW",  "lang": "TW"},
    "Google-Sa-CP-JP": {"old_ag": "Postman-JP",  "lang": "JP"},
    "Google-Sa-CP-VN": {"old_ag": "Postman-VN",  "lang": "VN"},
    "Google-Sa-CP-ID": {"old_ag": "Postman-ID",  "lang": "ID"},
    "Google-Sa-CP-PT": {"old_ag": "Postman-PT",  "lang": "PT"},
    "Google-Sa-CP-KR": {"old_ag": "Postman-KR",  "lang": "KR"},
    "Google-Sa-CP-DE": {"old_ag": "Postman-DE",  "lang": "DE"},
    "Google-Sa-CP-ar": {"old_ag": "Postman-AR",  "lang": "ar"},  # Arabic
    "Google-Sa-CP-AR": {"old_ag": "Postman-AR",  "lang": "ES"},  # Argentina (Spanish)
}

# Creatives by language
LANGUAGE_CREATIVES = {
    "ES": {
        "final_url": "https://apidog.com/es/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Alternativas a Postman", "Apidog: Mejor Alternativa", "Prueba API Gratis 2026", "Migración 1-Clic Postman", "Herramienta API Todo en Uno", "Sin Límites de Ejecución", "Documentación API Automática", "Plataforma OpenAPI 3.1", "Mock Server Gratis", "Diseño de API Colaborativo", "Apidog en Español", "Cliente HTTP Avanzado", "Alternativa Postman Gratis", "Workspace de API Equipo", "Generador de Docs API"],
            "descriptions": ["Reemplaza Postman con Apidog. Diseña, prueba, simula y documenta APIs en una plataforma.", "Importa tus colecciones de Postman sin pérdidas. Comienza gratis hoy mismo.", "Colaboración en equipo gratuita sin restricciones. Plataforma API moderna para equipos.", "Desarrolla APIs 10 veces más rápido con Apidog. Alternativa a Postman totalmente gratis."],
            "path1": "compare", "path2": "postman"
        }
    },
    "FR": {
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Alternative à Postman", "Plateforme API All-in-One", "Test API & Mock Gratuit", "Migration Postman en 1-Clic", "Documentation API Auto", "Collaboration Gratuite", "Sans Limites d'Exécution", "Client HTTP & Test API", "Alternative Postman Gratuite", "Générateur de Docs API", "Workspace API Tout-en-Un", "Support Native OpenAPI 3.1", "Mock Server API Intelligent", "Import de Collections Postman", "Plateforme API Gratuite"],
            "descriptions": ["Remplacez Postman par Apidog. Concevez, testez et documentez vos API sur une plateforme.", "Importez vos collections Postman en 1 clic sans perte de données. Essayez gratuitement.", "Tests d'API automatisés et serveurs mock sans limites d'exécution pour votre équipe.", "Outil de développement API moderne pour les développeurs en France et Europe."],
            "path1": "compare", "path2": "postman"
        }
    },
    "TW": {
        "final_url": "https://apidog.com/tw/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Postman 最佳替代方案 Apidog", "一站式 API 開發測試平台", "免費 API 測試與 Mock", "1 鍵匯入 Postman 資料", "自動生成 API 文件", "團隊協作完全免費", "無執行次數限制 API 測試", "繁體中文 API 開發工具", "Apidog 繁體中文版", "API 設計與調試整合", "Postman 免費替代軟體", "OpenAPI 3.1 原生支援", "智慧 API Mock 伺服器", "Postman 集合無縫轉移", "免費 API 用戶端工具"],
            "descriptions": ["全面替代 Postman。提供 API 設計、調試、測試與文檔一體化解決方案。", "一鍵無縫轉移 Postman 集合，無執行次數限制。立即免費使用。", "團隊免費協作，支援 API 自動化測試與 Mock 服務。提高開發效率。", "專為台灣及華人開發者打造的繁體中文一站式 API 開發平台."],
            "path1": "compare", "path2": "postman"
        }
    },
    "JP": {
        "final_url": "https://apidog.com/jp/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Postmanの代替ツール Apidog", "総合API開発プラットフォーム", "無料APIテスト＆モック", "Postmanデータ1クリック移行", "APIドキュメント自動生成", "チームコラボレーション無料", "実行回数無制限のAPIテスト", "日本語対応API開発ツール", "Apidog 日本語公式", "API設計・テスト・文書化", "Postman 無料 代替", "OpenAPI 3.1 完全対応", "APIモックサーバー自動作成", "Postmanコレクション移行", "無料APIクライアントツール"],
            "descriptions": ["Postmanからの移行ならApidog。API設計・テスト・モック・ドキュメント作成を一体化。", "ワンクリックでPostmanコレクションを完全移行。チームコラボレーション無料。", "実行回数制限なしのAPIテスト＆スマートモック。今すぐ無料で体験してください。", "日本市場向けの完全日本語化API開発プラットフォーム。開発効率を大幅向上。"],
            "path1": "compare", "path2": "postman"
        }
    },
    "VN": {
        "final_url": "https://apidog.com/vi/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Công Cụ Thay Thế Postman", "Nền Tảng API Tất-Cả-Trong-Một", "Kiểm Thử API Miễn Phí", "Chuyển Dữ Liệu Postman 1 Click", "Tự Động Tạo Tài Liệu API", "Cộng Tác Nhóm Miễn Phí", "Test API Không Giới Hạn", "Công Cụ API Tiếng Việt", "Apidog Tiếng Việt Official", "Thiết Kế & Kiểm Thử API", "Thay Thế Postman Miễn Phí", "Hỗ Trợ OpenAPI 3.1 Native", "Tạo Smart Mock Server API", "Nhập Collection Postman", "Công Cụ API Client Miễn Phí"],
            "descriptions": ["Thay thế Postman bằng Apidog. Thiết kế, kiểm thử, mock và tài liệu trên 1 nền tảng.", "Nhập bộ sưu tập Postman dễ dàng chỉ với 1 click. Sử dụng miễn phí ngay.", "Cộng tác nhóm miễn phí không giới hạn số lượt chạy test script. Nâng cao năng suất.", "Nền tảng phát triển API hỗ trợ tiếng Việt dành riêng cho lập trình viên Việt Nam."],
            "path1": "compare", "path2": "postman"
        }
    },
    "ID": {
        "final_url": "https://apidog.com/id/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Alternatif Postman Terbaik", "Platform API All-in-One", "Pengujian API Gratis Online", "Impor Postman 1-Klik", "Dokumentasi & Mock API", "Kolaborasi Tim Gratis", "Tanpa Batas Eksekusi Runner", "Alat Pengembang API Indonesia", "Apidog Bahasa Indonesia", "Desain dan Uji API Terpadu", "Software Alternatif Postman", "Dukungan Native OpenAPI 3.1", "Server Mock API Otomatis", "Transfer Koleksi Postman", "Client API Gratis Terbaik"],
            "descriptions": ["Gantikan Postman dengan Apidog. Desain, uji, mock, dan dokumentasikan API dalam satu alat.", "Impor koleksi Postman Anda dalam 1 klik tanpa batas eksekusi. Mulai gratis.", "Kolaborasi tim gratis dengan server mock dan pengujian otomatis tanpa biaya.", "Platform API mendukung Bahasa Indonesia untuk pengembang di Indonesia."],
            "path1": "compare", "path2": "postman"
        }
    },
    "PT": {
        "final_url": "https://apidog.com/pt/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Alternativa ao Postman", "Plataforma de API Tudo-em-Um", "Testar API Online Grátis", "Importar Postman em 1 Clique", "Documentação e Mock de API", "Design de API Colaborativo", "Sem Limites de Execução", "Cliente HTTP e Testes API", "Apidog em Português Grátis", "Gerador de Docs API Grátis", "Postman Grátis Alternativa", "Workspace de API em Equipe", "Testes de API Automatizados", "Importar Coleções do Postman", "Apidog Brasil e Portugal"],
            "descriptions": ["Substitua o Postman pelo Apidog. Teste, documente e simule APIs em uma plataforma.", "Migre suas coleções do Postman sem perdas. Sem limites de execução em equipe.", "Testes de API, servidores mock e documentação em um só lugar. Comece grátis hoje.", "Ferramenta API nativa em português para desenvolvedores no Brasil e Portugal."],
            "path1": "compare", "path2": "postman"
        }
    },
    "KR": {
        "final_url": "https://apidog.com/kr/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Postman 최고의 대체툴 Apidog", "올인원 API 개발 플랫폼", "무료 API 테스트 및 목서버", "Postman 1클릭 마이그레이션", "자동 API 문서 생성기", "팀 협업 완전 무료", "제한 없는 API 테스트", "한국어 지원 API 개발 툴", "Apidog 공식 한국어", "API 설계 및 테스트 통합", "Postman 무료 대체 솔루션", "OpenAPI 3.1 지원", "스마트 API 목 서버", "Postman 컬렉션 원클릭 이전", "무료 API 클라이언트"],
            "descriptions": ["Postman을 대체할 통합 API 툴 Apidog. API 설계, 테스트, 문서화를 한곳에서.", "원클릭으로 Postman 데이터를 손실 없이 이전하세요. 지금 무료 시작.", "러너 실행 제한 없는 무료 팀 협업 API 플랫폼. 개발 생산성을 높이세요.", "한국 개발자를 위한 완전 한국어 지원 API 개발 및 테스트 플랫폼."],
            "path1": "compare", "path2": "postman"
        }
    },
    "DE": {
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Postman Alternative 2026", "All-in-One API Platform", "Kostenloses API Testing", "1-Klick Postman Migration", "OpenAPI 3.1 Native Platform", "Keine Runner Ausführungslimits", "Automatische API Dokus", "Datenschutz & SOC2 Konform", "Postman Alternative Tool", "Kostenlose Team Kollaboration", "Automatisierte API Tests", "Smart Mock API Server", "Postman Kollektionen Import", "Integrierter API Workspace", "Apidog API Platform Gratis"],
            "descriptions": ["Ersetzen Sie Postman durch Apidog. API-Design, Testing, Mocking in einer Plattform.", "Importieren Sie Postman-Kollektionen nahtlos mit 1 Klick. Jetzt kostenlos testen.", "Kostenlose Team-Kollaboration ohne Beschränkungen bei Testausführungen.", "Moderne API-Entwicklungsplattform für Entwickler in Deutschland, Österreich & Schweiz."],
            "path1": "compare", "path2": "postman"
        }
    },
    "ar": {
        "final_url": "https://apidog.com/compare/apidog-vs-postman/",
        "rsa": {
            "headlines": ["Best Postman Alternative 2026", "Apidog: All-in-One API Tool", "Free API Testing & Mocking", "1-Click Postman Migration", "OpenAPI 3.1 Native Platform", "No Runner Execution Limits", "API Docs Generator", "Local-First API Workspace", "Postman Alternative Tool", "Free Team API Collaboration", "Automated API Testing Tool", "Smart Mock API Server", "Import Postman Collections", "All-in-One API Workspace", "Apidog API Platform Free"],
            "descriptions": ["Replace Postman with Apidog. Design, test, mock, and document APIs in one workspace.", "Import Postman collections effortlessly with zero data loss. Start for free today.", "Free team collaboration with no paywalls on runner executions or collection size.", "Modern OpenAPI 3.1 native API client for developers in Middle East & North Africa."],
            "path1": "compare", "path2": "postman"
        }
    }
}

def execute_operations():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    ag_service = client.get_service('AdGroupService')
    aga_service = client.get_service('AdGroupAdService')

    print(">>> Fetching all Ad Groups for target campaigns...")
    query = """
        SELECT campaign.id, campaign.name, ad_group.id, ad_group.name, ad_group.status
        FROM ad_group
        WHERE campaign.name LIKE '%Google-Sa-CP-%'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=query)
    
    ag_ops = []
    rsa_ops = []
    
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            ag_status = row.ad_group.status.name
            ag_id = row.ad_group.id
            ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
            
            # Action 1: Pause 2026 Ad Groups
            if "Postman-Alternative-" in ag_name and "-2026" in ag_name:
                if ag_status != "PAUSED":
                    print(f"Pausing 2026 Ad Group: {ag_name} in {c_name}")
                    ag_op = client.get_type('AdGroupOperation')
                    ag_op.update.resource_name = ag_path
                    ag_op.update.status = client.enums.AdGroupStatusEnum.PAUSED
                    ag_op.update_mask.paths.append("status")
                    ag_ops.append(ag_op)
            
            # Action 2: Enable specific Old Ad Groups and add Creatives
            if c_name in CAMPAIGN_MAPPING:
                mapping = CAMPAIGN_MAPPING[c_name]
                if mapping["old_ag"] == ag_name:
                    if ag_status != "ENABLED":
                        print(f"Enabling Old Ad Group: {ag_name} in {c_name}")
                        ag_op = client.get_type('AdGroupOperation')
                        ag_op.update.resource_name = ag_path
                        ag_op.update.status = client.enums.AdGroupStatusEnum.ENABLED
                        ag_op.update_mask.paths.append("status")
                        ag_ops.append(ag_op)
                        
                    # Add Creatives for this language
                    lang = mapping["lang"]
                    if lang in LANGUAGE_CREATIVES:
                        cfg = LANGUAGE_CREATIVES[lang]
                        aga_op = client.get_type('AdGroupAdOperation')
                        aga = aga_op.create
                        aga.ad_group = ag_path
                        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
                        aga.ad.final_urls.append(cfg["final_url"])
                        
                        rsa = aga.ad.responsive_search_ad
                        rsa.path1 = shorten(cfg["rsa"]["path1"], 15)
                        rsa.path2 = shorten(cfg["rsa"]["path2"], 15)
                        
                        for hl in cfg["rsa"]["headlines"][:15]:
                            headline = client.get_type('AdTextAsset')
                            headline.text = shorten(hl, 30)
                            rsa.headlines.append(headline)
                            
                        for desc in cfg["rsa"]["descriptions"][:4]:
                            description = client.get_type('AdTextAsset')
                            description.text = shorten(desc, 90)
                            rsa.descriptions.append(description)
                            
                        rsa_ops.append(aga_op)

    if ag_ops:
        print(f">>> Updating {len(ag_ops)} Ad Group Statuses...")
        ag_req = client.get_type('MutateAdGroupsRequest')
        ag_req.customer_id = CUSTOMER_ID
        ag_req.operations.extend(ag_ops)
        ag_req.partial_failure = True
        ag_resp = ag_service.mutate_ad_groups(request=ag_req)
        if ag_resp.partial_failure_error and ag_resp.partial_failure_error.details:
            for error in ag_resp.partial_failure_error.details:
                print(f"AdGroup Status Partial Failure: {error}")
                
    if rsa_ops:
        print(f">>> Uploading {len(rsa_ops)} new RSAs to old Ad Groups...")
        rsa_req = client.get_type('MutateAdGroupAdsRequest')
        rsa_req.customer_id = CUSTOMER_ID
        rsa_req.operations.extend(rsa_ops)
        rsa_req.partial_failure = True
        rsa_resp = aga_service.mutate_ad_group_ads(request=rsa_req)
        
        if rsa_resp.partial_failure_error and rsa_resp.partial_failure_error.details:
            for error in rsa_resp.partial_failure_error.details:
                print(f"RSA Partial Failure: {error}")
        else:
            print(f"RSAs Success! Uploaded {len(rsa_resp.results)} RSAs to old Ad Groups.")

    return True

def main():
    max_retries = 15
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            if execute_operations():
                print("[SUCCESS] All Pivot Operations Finished!")
                break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == '__main__':
    main()
