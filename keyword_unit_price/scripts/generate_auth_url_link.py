import os
import yaml
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

YAML_PATH = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'

with open(YAML_PATH, 'r') as f:
    config = yaml.safe_load(f)

client_config = {
    "installed": {
        "client_id": config.get('client_id'),
        "client_secret": config.get('client_secret'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

scopes = ["https://www.googleapis.com/auth/adwords"]
flow = InstalledAppFlow.from_client_config(client_config, scopes)
flow.redirect_uri = "http://localhost:8085/"

auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

print("URL_START")
print(auth_url)
print("URL_END")

with open("d:/Apidog Work/Google ADS Keywords Unit Price/common/config/auth_url.txt", "w") as f:
    f.write(auth_url)
