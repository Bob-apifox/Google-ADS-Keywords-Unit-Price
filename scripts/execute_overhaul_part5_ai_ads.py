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
URL_SUFFIX = "utm_source=google_search&utm_medium=cpc&utm_campaign={campaignid}&utm_term={keyword}"

def get_len(text):
    return sum(2 if ord(c) > 127 else 1 for c in text)

def shorten(text, max_len):
    while get_len(text) > max_len:
        text = text[:-1]
    return text.strip()

# 3 Themes, 15 H1 + 4 Desc each
ADS_CONFIG = {
    "Google-Sa-CP-AR": {
        "url": "https://apidog.com/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Postman Alternative", "Apidog API Tool", "1-Click Migration", "Switch from Postman", "Best Postman Alt", "Replace Postman", "Postman Free Alt", "API Migration", "Export Postman", "Postman Importer", "Postman vs Apidog", "Apidog for AR", "Easy Postman Sync", "Better API Tool", "Upgrade API Tool"],
            "desc": ["Switch from Postman to Apidog easily. Import collections in one click.", "Best Postman alternative for Arabic developers. Try Apidog today.", "Say goodbye to Postman sync issues. Migrate to Apidog for free.", "The ultimate Postman replacement. Upgrade your API workflow now."]
        },
        "B": {
            "hl": ["All-in-One API Tool", "API Testing Tool", "Smart Mock Server", "API Docs Generator", "OpenAPI 3.1 Support", "Design API Fast", "Automated Testing", "API Mocking Tool", "API Development", "Test APIs Free", "Mock API Server", "Apidog Testing", "Debug APIs Easily", "API Client Tool", "API Life Cycle"],
            "desc": ["Design, test, mock, and document APIs in one unified workspace.", "Generate beautiful API docs automatically. Support OpenAPI 3.1.", "Create smart mock servers in seconds without coding. Try it free.", "Automate your API testing workflow with powerful assertions."]
        },
        "C": {
            "hl": ["Free API Workspace", "No Runner Limits", "Team Collaboration", "Free Team API Tool", "Unlimited API Tests", "Free Postman Alt", "Apidog Free Tier", "API Team Sync", "Free API Mocking", "Collaborate Free", "No Paywalls", "Unlimited Runs", "API Tool for Teams", "Cost-Free API App", "Apidog Free Teams"],
            "desc": ["Free team collaboration with no paywalls on runner executions.", "Stop paying for Postman runner limits. Apidog is free for teams.", "Collaborate with your backend and frontend teams seamlessly.", "Enjoy unlimited API testing and mocking without hidden fees."]
        }
    },
    "Google-Sa-CP-PT": {
        "url": "https://apidog.com/pt/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Alternativa ao Postman", "Migrar do Postman", "Apidog vs Postman", "Importar em 1 Clique", "Mudar para Apidog", "Substituto Postman", "Melhor que Postman", "Postman Grátis Alt", "Importar Coleções", "Apidog Brasil", "Apidog Portugal", "Trocar de API Tool", "Alternativa Postman", "Postman Exporte", "Postman Migration"],
            "desc": ["Substitua o Postman pelo Apidog. Importe coleções em 1 clique grátis.", "A melhor alternativa ao Postman para desenvolvedores no Brasil.", "Mude para o Apidog e evite problemas de sincronização do Postman.", "Migre seus dados do Postman sem perdas. Comece a usar hoje."]
        },
        "B": {
            "hl": ["Plataforma API Tudo", "Testar API Online", "Mock Server Grátis", "Gerador Docs API", "Suporte OpenAPI 3", "Cliente HTTP", "Teste API Auto", "Design API Fácil", "Apidog Testes", "Simular APIs", "Ferramenta API PT", "Desenvolver APIs", "Mocking API", "Debug de API", "API All-in-One"],
            "desc": ["Teste, documente e simule APIs em uma plataforma tudo-em-um.", "Gere documentação de API automaticamente com suporte OpenAPI 3.1.", "Crie mock servers inteligentes em segundos. Totalmente gratuito.", "Automatize seus testes de API com o melhor cliente HTTP."]
        },
        "C": {
            "hl": ["Workspace API Equipe", "Sem Limites Run", "Colaboração Grátis", "Equipes API Grátis", "Sem Paywalls", "Apidog Grátis", "API Ilimitada", "Testes Ilimitados", "Colaborar Equipe", "Ferramenta Equipes", "Mocking Gratuito", "Teste API Ilimitado", "Trabalho em Equipe", "Apidog Free", "Uso Sem Limites"],
            "desc": ["Colaboração em equipe gratuita sem limites de execução de testes.", "Pare de pagar caro no Postman. Apidog é grátis para equipes.", "Trabalhe junto com sua equipe frontend e backend perfeitamente.", "Desfrute de testes e mocks de API ilimitados sem taxas."]
        }
    },
    "Google-Sa-CP-JP": {
        "url": "https://apidog.com/jp/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Postmanの代替ツール", "Apidogへ移行", "1クリックで移行", "Postman代替", "Postmanより便利", "Postman無料代替", "APIデータ移行", "Postmanインポート", "Apidog 日本語", "無料で乗り換え", "最高の代替ツール", "Postmanコレクション", "APIツール変更", "Apidog vs Postman", "Postman卒業"],
            "desc": ["Postmanからの移行ならApidog。1クリックでデータを完全移行。", "日本の開発者向けPostman代替ツール。今すぐ無料でお試し。", "同期エラーに悩まない。Apidogへ無料でシームレスに移行。", "Postmanのコレクションを損失なしで簡単にインポート可能。"]
        },
        "B": {
            "hl": ["総合APIツール", "APIテストツール", "モックサーバー作成", "API仕様書自動生成", "OpenAPI 3.1対応", "高速API設計", "自動APIテスト", "日本語APIツール", "API開発プラットフォーム", "スマートモック", "APIドキュメント", "HTTPクライアント", "APIデバッグ", "API自動化", "Apidogテスト"],
            "desc": ["API設計、テスト、モック、仕様書生成を1つのツールに統合。", "OpenAPI 3.1対応の美しいAPIドキュメントを自動生成します。", "コーディング不要でスマートなAPIモックを数秒で作成可能。", "強力なHTTPクライアントでAPIテストを完全に自動化します。"]
        },
        "C": {
            "hl": ["チームコラボ無料", "実行回数無制限", "無料APIツール", "制限なしAPIテスト", "無料モックサーバー", "完全無料チーム", "APIチーム共有", "課金の壁なし", "無制限テスト", "Apidog無料版", "チーム開発ツール", "制限なし実行", "フロントエンド連携", "追加料金なし", "無制限API開発"],
            "desc": ["実行回数の制限なし！チームコラボレーションが完全に無料。", "Postmanの高額な課金は不要。Apidogはチーム開発に最適。", "フロントエンドとバックエンドのチーム連携をシームレスに。", "隠れた費用なしで、無制限のAPIテストとモックを利用可能。"]
        }
    },
    "Google-Sa-CP-KR": {
        "url": "https://apidog.com/kr/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Postman 대체툴", "Apidog 마이그레이션", "1클릭 데이터 이전", "Postman 대체", "최고의 Postman 대안", "Postman 무료 대체", "API 데이터 마이그", "Postman 임포트", "Apidog 한국어", "무료로 갈아타기", "완벽한 대체 툴", "Postman 컬렉션", "API 툴 변경", "Apidog vs Postman", "Postman 졸업"],
            "desc": ["Postman에서 Apidog로 전환하세요. 1클릭으로 데이터 완벽 이전.", "한국 개발자를 위한 최고의 Postman 대체 툴. 무료로 시작.", "동기화 오류 없이 Apidog로 원활하게 마이그레이션하세요.", "Postman 컬렉션을 손실 없이 쉽게 가져올 수 있습니다."]
        },
        "B": {
            "hl": ["올인원 API 툴", "API 테스트 툴", "스마트 목 서버", "API 문서 자동생성", "OpenAPI 3.1 지원", "빠른 API 설계", "자동화 API 테스트", "한국어 API 툴", "API 개발 플랫폼", "API 모킹 서버", "API 명세서", "HTTP 클라이언트", "API 디버깅", "API 테스트 자동화", "Apidog 테스트"],
            "desc": ["API 설계, 테스트, 목업, 문서 생성을 하나의 툴로 통합.", "OpenAPI 3.1을 지원하는 아름다운 API 문서를 자동 생성하세요.", "코딩 없이 스마트 API 목 서버를 몇 초 만에 만드세요.", "강력한 HTTP 클라이언트로 API 테스트를 완벽하게 자동화."]
        },
        "C": {
            "hl": ["팀 협업 완전 무료", "실행 횟수 무제한", "무료 API 툴", "제한없는 API테스트", "무료 목업 서버", "완전 무료 팀워크", "API 팀 공유", "페이월 없음", "무제한 테스트", "Apidog 무료티어", "팀 개발 도구", "무제한 실행", "프론트엔드 협업", "추가 요금 없음", "무제한 API개발"],
            "desc": ["실행 횟수 제한 없는 완전 무료 팀 협업 API 플랫폼.", "Postman의 비싼 요금제 대신 Apidog로 팀 개발을 시작하세요.", "프론트엔드와 백엔드 팀 간의 완벽한 API 협업을 지원합니다.", "숨겨진 비용 없이 무제한 API 테스트 및 모킹을 즐기세요."]
        }
    },
    "Google-Sa-CP-TW": {
        "url": "https://apidog.com/tw/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Postman 替代方案", "1鍵匯入 Postman", "無縫轉移 Apidog", "取代 Postman", "Postman 免費替代", "API 資料轉移", "匯入 Postman", "Apidog 繁體中文", "免費更換 API 軟體", "最佳替代工具", "Postman 集合匯入", "換掉 Postman", "Apidog vs Postman", "告別 Postman", "最強替代品"],
            "desc": ["從 Postman 轉移到 Apidog，一鍵無縫匯入所有資料。", "專為台灣開發者打造的 Postman 最佳替代方案，立即免費試用。", "告別 Postman 同步問題，輕鬆升級你的 API 開發流程。", "完整保留 Postman 集合資料，輕鬆轉換無痛上手。"]
        },
        "B": {
            "hl": ["一站式 API 工具", "API 測試軟體", "智慧 Mock 伺服器", "API 文件自動生成", "OpenAPI 3.1 支援", "極速 API 設計", "自動化 API 測試", "繁中 API 工具", "API 開發平台", "API Mocking", "自動 API 說明檔", "HTTP 用戶端", "API 除錯工具", "自動測試 API", "Apidog 測試"],
            "desc": ["將 API 設計、測試、Mock 和文件整合在一個完美的工作站。", "支援 OpenAPI 3.1，自動產生精美且易讀的 API 說明文件。", "免寫程式碼，幾秒鐘內即可建立智慧 API Mock 伺服器。", "強大的 HTTP 用戶端，讓你的 API 測試流程完全自動化。"]
        },
        "C": {
            "hl": ["團隊協作完全免費", "無測試執行限制", "免費 API 團隊", "無上限 API 測試", "免費 Mock 伺服器", "免費團隊開發", "API 團隊共用", "無隱藏收費", "無限次數測試", "Apidog 免費版", "團隊協作工具", "執行次數無限", "前後端無縫協作", "免付費無限制", "無限 API 開發"],
            "desc": ["團隊協作完全免費，打破 Postman 測試執行次數限制。", "別再付高昂的 Postman 費用，Apidog 讓團隊免費無痛使用。", "完美串聯前端與後端團隊，讓 API 開發與協作變得更簡單。", "沒有任何隱藏費用，盡情享受無限次數的 API 測試與 Mock。"]
        }
    },
    "Google-Sa-CP-VN": {
        "url": "https://apidog.com/vi/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Thay thế Postman", "Chuyển sang Apidog", "Nhập Postman 1 Click", "Giải pháp thay thế", "Thay thế miễn phí", "Chuyển dữ liệu API", "Nhập Collection", "Apidog Tiếng Việt", "Đổi công cụ API", "Công cụ thay thế", "Nhập dữ liệu Postman", "Thay thế hoàn hảo", "Apidog vs Postman", "Tạm biệt Postman", "Công cụ tốt nhất"],
            "desc": ["Chuyển từ Postman sang Apidog dễ dàng. Nhập dữ liệu chỉ 1 click.", "Giải pháp thay thế Postman tốt nhất cho lập trình viên Việt Nam.", "Nói lời tạm biệt với lỗi đồng bộ. Chuyển sang Apidog miễn phí.", "Nhập trọn vẹn collection Postman của bạn mà không mất dữ liệu."]
        },
        "B": {
            "hl": ["Công cụ API All-in", "Công cụ test API", "Smart Mock Server", "Tạo tài liệu API", "Hỗ trợ OpenAPI 3.1", "Thiết kế API nhanh", "Test API tự động", "Công cụ API VN", "Nền tảng phát triển", "Server Mock API", "API Documentation", "HTTP Client tốt", "Debug API dễ dàng", "Tự động hóa Test", "Apidog Testing"],
            "desc": ["Thiết kế, kiểm thử, mock và tạo tài liệu API trên một nền tảng.", "Tự động tạo tài liệu API tuyệt đẹp với hỗ trợ OpenAPI 3.1.", "Tạo smart mock server trong vài giây mà không cần viết code.", "Tự động hóa quy trình kiểm thử API với HTTP client mạnh mẽ."]
        },
        "C": {
            "hl": ["Làm việc nhóm Free", "Không giới hạn Run", "Team API miễn phí", "Test API không hạn", "Mock Server Free", "Làm việc nhóm 0đ", "Chia sẻ API Team", "Không có Paywall", "Test không giới hạn", "Apidog bản miễn phí", "Công cụ cho Team", "Run không giới hạn", "Team Frontend Backend", "Không phí ẩn", "Phát triển API Free"],
            "desc": ["Cộng tác nhóm hoàn toàn miễn phí, không giới hạn lượt chạy test.", "Ngừng trả tiền cho giới hạn của Postman. Apidog miễn phí cho team.", "Cộng tác giữa nhóm frontend và backend của bạn một cách liền mạch.", "Tận hưởng kiểm thử và mock API không giới hạn không có phí ẩn."]
        }
    },
    "Google-Sa-CP-ID": {
        "url": "https://apidog.com/id/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Alternatif Postman", "Pindah ke Apidog", "Impor 1 Klik Postman", "Ganti Postman Gratis", "Alternatif Terbaik", "Transfer Data API", "Impor Koleksi", "Apidog Indonesia", "Ubah Alat API", "Pengganti Postman", "Impor Data Postman", "Apidog vs Postman", "Tinggalkan Postman", "Pindah Sekarang", "Alat Migrasi API"],
            "desc": ["Pindah dari Postman ke Apidog. Impor koleksi hanya dengan 1 klik.", "Alternatif Postman terbaik untuk developer di Indonesia.", "Ucapkan selamat tinggal pada masalah sinkronisasi Postman.", "Impor seluruh koleksi Postman Anda tanpa kehilangan data."]
        },
        "B": {
            "hl": ["Alat API All-in-One", "Alat Testing API", "Smart Mock Server", "Generator Dokumen", "Dukungan OpenAPI 3", "Desain API Cepat", "Testing Otomatis", "Alat API Indonesia", "Platform Dev API", "Server Mock API", "Dokumentasi API", "Client HTTP API", "Debug API Mudah", "Otomatisasi Testing", "Testing Apidog"],
            "desc": ["Desain, uji, mock, dan dokumentasikan API dalam satu platform.", "Buat dokumentasi API otomatis yang mendukung OpenAPI 3.1.", "Buat server mock cerdas dalam hitungan detik tanpa coding.", "Otomatisasi alur kerja pengujian API Anda dengan alat terbaik."]
        },
        "C": {
            "hl": ["Kolaborasi Tim Gratis", "Tanpa Batas Eksekusi", "Tim API Gratis", "Testing Tanpa Batas", "Mock Server Gratis", "Kerja Tim Gratis", "Berbagi API Tim", "Tanpa Biaya Ekstra", "Uji Tanpa Batas", "Apidog Versi Gratis", "Alat Untuk Tim", "Eksekusi Unlimited", "Kolaborasi Frontend", "Tanpa Biaya Sembunyi", "API Dev Unlimited"],
            "desc": ["Kolaborasi tim gratis tanpa batas eksekusi runner test.", "Berhenti membayar limit Postman. Apidog gratis untuk tim.", "Berkolaborasi dengan tim frontend dan backend secara mulus.", "Nikmati testing dan mocking API tanpa batas tanpa biaya tersembunyi."]
        }
    },
    "Google-Sa-CP-DE": {
        "url": "https://apidog.com/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Postman Alternative", "Wechsel zu Apidog", "1-Klick Migration", "Postman Ersetzen", "Beste Alternative", "Postman Gratis Alt", "API Daten Umzug", "Kollektionen Import", "Apidog auf Deutsch", "API Tool Wechseln", "Postman Importeur", "Apidog vs Postman", "Tschüss Postman", "Besseres API Tool", "Einfacher Umzug"],
            "desc": ["Wechseln Sie von Postman zu Apidog. 1-Klick Daten-Import.", "Die beste Postman Alternative für Entwickler in Deutschland.", "Vermeiden Sie Postman-Sync-Probleme. Gratis zu Apidog wechseln.", "Importieren Sie Postman-Kollektionen ohne Datenverlust."]
        },
        "B": {
            "hl": ["All-in-One API Tool", "API Testing Tool", "Smart Mock Server", "API Dokus Generator", "OpenAPI 3.1 Support", "API Schnell Design", "Automatisiertes Test", "Deutsches API Tool", "API Entwicklung", "API Mock Server", "API Dokumentation", "HTTP Client", "APIs Debuggen", "Test Automatisierung", "Apidog Testing"],
            "desc": ["Designen, testen, mocken und dokumentieren Sie APIs an einem Ort.", "Erstellen Sie schöne API-Dokumentationen mit OpenAPI 3.1 Support.", "Intelligente Mock-Server in Sekunden erstellen, ohne Code.", "Automatisieren Sie Ihren API-Testing-Workflow effizient."]
        },
        "C": {
            "hl": ["Gratis Team Workspace", "Keine Runner Limits", "Team Kollaboration", "Kostenloses API Tool", "Unbegrenzte Tests", "Gratis Mock Server", "API Team Sharing", "Keine Paywalls", "Testen Ohne Limit", "Apidog Gratis Tier", "Werkzeug Für Teams", "Unbegrenzte Runs", "Frontend & Backend", "Keine Versteckten", "API Ohne Limits"],
            "desc": ["Kostenlose Team-Kollaboration ohne Limits bei Testausführungen.", "Zahlen Sie nicht mehr für Postman-Limits. Apidog ist gratis.", "Nahtlose Zusammenarbeit zwischen Frontend- und Backend-Teams.", "Nutzen Sie API Testing und Mocking ohne versteckte Gebühren."]
        }
    },
    "Google-Sa-CP-FR": {
        "url": "https://apidog.com/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Alternative à Postman", "Passer à Apidog", "Migration en 1 Clic", "Remplacer Postman", "Meilleure Alternative", "Alternative Gratuite", "Migration de Données", "Import Collections", "Apidog en Français", "Changer d'Outil API", "Importateur Postman", "Apidog vs Postman", "Adieu Postman", "Outil API Supérieur", "Migration Facile"],
            "desc": ["Passez de Postman à Apidog. Importez en 1 clic sans effort.", "La meilleure alternative à Postman pour les développeurs.", "Dites adieu aux bugs de Postman. Passez à Apidog gratuitement.", "Importez vos collections Postman sans aucune perte de données."]
        },
        "B": {
            "hl": ["Outil API Tout-en-Un", "Outil Test API", "Mock Server Smart", "Générateur Docs API", "Support OpenAPI 3.1", "Conception Rapide", "Tests Automatisés", "Outil API Français", "Plateforme API", "Serveur Mock API", "Documentation API", "Client HTTP", "Débogage API Facile", "Tests Auto API", "Testing Apidog"],
            "desc": ["Concevez, testez, mockez et documentez vos API au même endroit.", "Générez des docs API magnifiques avec le support OpenAPI 3.1.", "Créez des mock servers intelligents en quelques secondes.", "Automatisez vos workflows de tests API avec un outil puissant."]
        },
        "C": {
            "hl": ["Espace Équipe Gratuit", "Sans Limite de Run", "Collaboration Équipe", "Outil API Gratuit", "Tests Illimités", "Mock Server Gratuit", "Partage Équipe API", "Aucun Paywall", "Test Sans Limite", "Apidog Gratuit", "Outil Pour Équipes", "Exécutions Illimitées", "Frontend et Backend", "Sans Frais Cachés", "API Sans Limites"],
            "desc": ["Collaboration gratuite en équipe sans limites d'exécution.", "Arrêtez de payer pour les limites de Postman. Apidog est gratuit.", "Collaborez parfaitement entre vos équipes frontend et backend.", "Profitez de tests et de mocks API illimités sans frais cachés."]
        }
    },
    "Google-Sa-CP-ESP-2": {
        "url": "https://apidog.com/es/compare/apidog-vs-postman/",
        "A": {
            "hl": ["Alternativa a Postman", "Cambiar a Apidog", "Migración 1 Clic", "Reemplazar Postman", "Mejor Alternativa", "Postman Alternativa", "Migrar Datos API", "Importar Colecciones", "Apidog en Español", "Cambiar Herramienta", "Importador Postman", "Apidog vs Postman", "Adiós Postman", "Mejor Herramienta API", "Migración Fácil"],
            "desc": ["Cambia de Postman a Apidog. Importa colecciones en 1 clic.", "La mejor alternativa a Postman para desarrolladores.", "Di adiós a los errores de Postman. Cámbiate a Apidog gratis.", "Importa tus colecciones de Postman sin perder ningún dato."]
        },
        "B": {
            "hl": ["API Todo en Uno", "Pruebas de API", "Mock Server Smart", "Docs API Automáticas", "Soporte OpenAPI 3.1", "Diseño API Rápido", "Pruebas Automáticas", "Herramienta API ES", "Plataforma Dev API", "Servidor Mock API", "Documentación API", "Cliente HTTP API", "Depuración API", "Automatizar Pruebas", "Testing con Apidog"],
            "desc": ["Diseña, prueba, mockea y documenta APIs en un solo lugar.", "Genera documentación API hermosa con soporte OpenAPI 3.1.", "Crea servidores mock inteligentes en segundos sin código.", "Automatiza tus flujos de prueba de API de manera eficiente."]
        },
        "C": {
            "hl": ["Equipo API Gratis", "Sin Límites de Run", "Colaboración Equipo", "Herramienta Gratis", "Pruebas Ilimitadas", "Mock Server Gratis", "Compartir API Equipo", "Sin Muros de Pago", "Test Sin Límites", "Apidog Nivel Gratis", "Para Equipos Dev", "Ejecución Ilimitada", "Frontend y Backend", "Sin Cargos Ocultos", "API Sin Límites"],
            "desc": ["Colaboración de equipo gratis sin límites de ejecución de test.", "Deja de pagar los límites de Postman. Apidog es gratis.", "Colabora sin problemas entre tus equipos frontend y backend.", "Disfruta de pruebas y mocks de API ilimitados sin pagos ocultos."]
        }
    }
}

def execute_ai_fix():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    aga_service = client.get_service('AdGroupAdService')
    
    # 1. Fetch the 10 Postman AdGroups
    q_ag = """
        SELECT ad_group.id, ad_group.name, campaign.name, campaign.id
        FROM ad_group
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag)
    
    ag_map = {}
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_name = row.ad_group.name
            ag_id = row.ad_group.id
            if 'postman' in ag_name.lower() and c_name != 'Google-Sa-CP-ar':
                ag_map[c_name] = (ag_id, ag_name)

    # 2. Pause the recently uploaded ads (all ENABLED ads)
    print(">>> Pausing all existing active ads in these groups...")
    q_ads = """
        SELECT ad_group_ad.ad.id, ad_group.id, campaign.name
        FROM ad_group_ad
        WHERE campaign.name LIKE '%Google-Sa-CP-%' AND ad_group.status = 'ENABLED' AND ad_group_ad.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads)
    ad_pause_ops = []
    for batch in stream:
        for row in batch.results:
            c_name = row.campaign.name
            ag_id = row.ad_group.id
            ad_id = row.ad_group_ad.ad.id
            if c_name in ag_map and ag_map[c_name][0] == ag_id:
                op = client.get_type('AdGroupAdOperation')
                ad = op.update
                ad.resource_name = aga_service.ad_group_ad_path(CUSTOMER_ID, ag_id, ad_id)
                ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
                op.update_mask.paths.append("status")
                ad_pause_ops.append(op)
                
    if ad_pause_ops:
        print(f"Pausing {len(ad_pause_ops)} active ads...")
        req = client.get_type('MutateAdGroupAdsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ad_pause_ops)
        req.partial_failure = True
        aga_service.mutate_ad_group_ads(request=req)

    # 3. Upload 3 Distinct RSAs per group with URL Suffix
    print(">>> Uploading 3 distinct themed RSAs...")
    rsa_ops = []
    
    for c_name, (ag_id, ag_name) in ag_map.items():
        if c_name not in ADS_CONFIG:
            continue
            
        cfg = ADS_CONFIG[c_name]
        ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
        
        themes = ['A', 'B', 'C']
        
        for t in themes:
            theme_cfg = cfg[t]
            aga_op = client.get_type('AdGroupAdOperation')
            aga = aga_op.create
            aga.ad_group = ag_path
            aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
            
            aga.ad.final_urls.append(cfg["url"])
            aga.ad.final_url_suffix = URL_SUFFIX
            
            rsa = aga.ad.responsive_search_ad
            rsa.path1 = shorten("compare", 15)
            rsa.path2 = shorten("postman", 15)
            
            for hl in theme_cfg["hl"][:15]:
                headline = client.get_type('AdTextAsset')
                headline.text = shorten(hl, 30)
                rsa.headlines.append(headline)
                
            # Need to append filler descriptions if less than 4
            descs = theme_cfg["desc"]
            # To make 4 distinct descriptions we might cycle them or take from other themes
            if len(descs) < 4:
                filler = cfg['B']['desc'] + cfg['A']['desc'] + cfg['C']['desc']
                for f in filler:
                    if f not in descs:
                        descs.append(f)
                    if len(descs) == 4:
                        break
                        
            for desc in descs[:4]:
                description = client.get_type('AdTextAsset')
                description.text = shorten(desc, 90)
                rsa.descriptions.append(description)
                
            rsa_ops.append(aga_op)
            
    if rsa_ops:
        print(f">>> Uploading {len(rsa_ops)} fully thematic RSAs...")
        req = client.get_type('MutateAdGroupAdsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(rsa_ops)
        req.partial_failure = True
        resp = aga_service.mutate_ad_group_ads(request=req)
        if resp.partial_failure_error and resp.partial_failure_error.details:
            for err in resp.partial_failure_error.details:
                print(f"RSA Error: {err}")
        else:
            print("Successfully uploaded all distinct RSAs!")

    print("[SUCCESS] AI Fix Execution Finished!")
    return True

def main():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt+1}/{max_retries}...")
            if execute_ai_fix():
                break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(3)

if __name__ == '__main__':
    main()
