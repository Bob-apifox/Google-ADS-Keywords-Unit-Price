import os
import sys
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

print("Starting local OAuth callback server on port 8085...")
credentials = flow.run_local_server(port=8085, prompt='consent', access_type='offline')

new_refresh_token = credentials.refresh_token
if new_refresh_token:
    config['refresh_token'] = new_refresh_token
    with open(YAML_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    print(f"[SUCCESS] New refresh token saved: {new_refresh_token[:15]}...")
else:
    print("[ERROR] Refresh token missing.")
