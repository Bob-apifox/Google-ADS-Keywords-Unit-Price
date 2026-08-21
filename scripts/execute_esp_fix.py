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

ESP_CONFIG = {
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

SPANISH_KEYWORDS = [
    "alternativa a postman", "mejores alternativas postman", "alternativa gratuita a postman", "herramientas como postman",
    "postman vs apidog", "reemplazo de postman", "alternativa de código abierto postman", "migrar de postman",
    "herramienta de prueba de api postman", "alternativa postman para equipo", "exportar colección postman", "importar a postman",
    "cliente api como postman", "alternativas a la colección postman", "entorno postman alternativa", "api rest postman",
    "software alternativo a postman", "postman online alternativa", "alternativa al escritorio de postman", "herramientas de documentación api postman",
    "apidog", "descargar apidog", "apidog online", "apidog web", "apidog vs postman",
    "precio de apidog", "descarga gratuita de apidog", "extensión apidog", "tutorial apidog", "revisión apidog",
    "apidog mac", "herramienta de prueba de api apidog", "apidog linux", "iniciar sesión apidog", "documentación apidog",
    "alternativa a apidog", "api de apidog", "cliente api", "herramienta de prueba de api", "herramientas de diseño de api",
    "herramientas de documentación api", "herramientas de desarrollo de api", "mejor cliente api", "cliente api rest", "herramienta simulador api",
    "software de prueba de api", "cliente api gratuito", "creador de api", "alternativa a swagger", "alternativa a insomnia",
    "soapui alternativa", "insomnia vs postman", "swagger vs postman", "plataforma api", "gestión del ciclo de vida de la api",
    "api rest prueba", "api graphql prueba", "api grpc prueba", "websocket prueba", "api automatizada prueba",
    "api generador de código", "api servidor de simulación", "servidor simulado gratuito", "documentación swagger", "openapi generador",
    "openapi 3.0", "herramienta json a api", "herramientas de colaboración api", "equipo api", "flujo de trabajo api",
    "pruebas de rendimiento de la api", "api herramientas de monitoreo", "herramientas de depuración de api", "postman para linux", "insomnia api",
    "descargar insomnia", "precio de insomnia", "extensión de cliente rest", "extensión postman chrome", "cliente avanzado rest"
]

def execute_esp_fix():
    client = GoogleAdsClient.load_from_storage(GOOGLE_ADS_YAML)
    ga_service = client.get_service('GoogleAdsService')
    aga_service = client.get_service('AdGroupAdService')
    agbc_service = client.get_service('AdGroupCriterionService')
    
    # 1. Fetch Google-Sa-CP-ESP ad groups
    q_ag = """
        SELECT ad_group.id, ad_group.name, campaign.name, campaign.id
        FROM ad_group
        WHERE campaign.name = 'Google-Sa-CP-ESP' AND ad_group.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ag)
    
    ag_id = None
    ag_name = None
    for batch in stream:
        for row in batch.results:
            if 'postman' in row.ad_group.name.lower():
                ag_id = row.ad_group.id
                ag_name = row.ad_group.name
                break
                
    if not ag_id:
        print("Could not find Postman ad group in Google-Sa-CP-ESP")
        return False
        
    print(f"Found Ad Group: {ag_name} ({ag_id}) in Google-Sa-CP-ESP")
    
    # 2. Pause old ads
    q_ads = f"""
        SELECT ad_group_ad.ad.id
        FROM ad_group_ad
        WHERE campaign.name = 'Google-Sa-CP-ESP' AND ad_group.id = {ag_id} AND ad_group_ad.status = 'ENABLED'
    """
    stream = ga_service.search_stream(customer_id=CUSTOMER_ID, query=q_ads)
    ad_pause_ops = []
    for batch in stream:
        for row in batch.results:
            op = client.get_type('AdGroupAdOperation')
            ad = op.update
            ad.resource_name = aga_service.ad_group_ad_path(CUSTOMER_ID, ag_id, row.ad_group_ad.ad.id)
            ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
            op.update_mask.paths.append("status")
            ad_pause_ops.append(op)
            
    if ad_pause_ops:
        print(f"Pausing {len(ad_pause_ops)} old ads...")
        req = client.get_type('MutateAdGroupAdsRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(ad_pause_ops)
        req.partial_failure = True
        aga_service.mutate_ad_group_ads(request=req)

    # 3. Upload 3 distinct RSAs
    print("Uploading 3 distinct AI RSAs...")
    rsa_ops = []
    ag_path = ga_service.ad_group_path(CUSTOMER_ID, ag_id)
    
    for t in ['A', 'B', 'C']:
        theme_cfg = ESP_CONFIG[t]
        aga_op = client.get_type('AdGroupAdOperation')
        aga = aga_op.create
        aga.ad_group = ag_path
        aga.status = client.enums.AdGroupAdStatusEnum.ENABLED
        
        aga.ad.final_urls.append(ESP_CONFIG["url"])
        aga.ad.final_url_suffix = URL_SUFFIX
        
        rsa = aga.ad.responsive_search_ad
        rsa.path1 = shorten("compare", 15)
        rsa.path2 = shorten("postman", 15)
        
        for hl in theme_cfg["hl"][:15]:
            headline = client.get_type('AdTextAsset')
            headline.text = shorten(hl, 30)
            rsa.headlines.append(headline)
            
        for desc in theme_cfg["desc"][:4]:
            description = client.get_type('AdTextAsset')
            description.text = shorten(desc, 90)
            rsa.descriptions.append(description)
            
        rsa_ops.append(aga_op)
        
    req = client.get_type('MutateAdGroupAdsRequest')
    req.customer_id = CUSTOMER_ID
    req.operations.extend(rsa_ops)
    req.partial_failure = True
    aga_service.mutate_ad_group_ads(request=req)
    
    # 4. Upload Keywords
    print("Uploading Spanish Keywords...")
    kw_ops = []
    for kw in SPANISH_KEYWORDS:
        for match_type in [client.enums.KeywordMatchTypeEnum.EXACT, client.enums.KeywordMatchTypeEnum.PHRASE]:
            op = client.get_type('AdGroupCriterionOperation')
            agc = op.create
            agc.ad_group = ag_path
            agc.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            agc.keyword.text = kw
            agc.keyword.match_type = match_type
            kw_ops.append(op)
            
    # Batch in 100s
    for i in range(0, len(kw_ops), 100):
        req = client.get_type('MutateAdGroupCriteriaRequest')
        req.customer_id = CUSTOMER_ID
        req.operations.extend(kw_ops[i:i+100])
        req.partial_failure = True
        agbc_service.mutate_ad_group_criteria(request=req)
        
    print("[SUCCESS] ESP Campaign fully fixed!")
    return True

if __name__ == '__main__':
    execute_esp_fix()
