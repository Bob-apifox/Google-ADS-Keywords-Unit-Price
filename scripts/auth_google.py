import os
import yaml
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

# Fix print encoding
sys.stdout.reconfigure(encoding='utf-8')

yaml_path = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'

with open(yaml_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

client_id = config.get('client_id')
client_secret = config.get('client_secret')

client_config = {
    "installed": {
        "client_id": client_id,
        "client_secret": client_secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
}

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

scopes = ["https://www.googleapis.com/auth/adwords"]
flow = InstalledAppFlow.from_client_config(client_config, scopes=scopes)

print("="*60)
print("Waiting for authorization...")
print("="*60)

creds = flow.run_local_server(port=8080, open_browser=False)

# Save FIRST
config['refresh_token'] = creds.refresh_token
with open(yaml_path, 'w', encoding='utf-8') as f:
    yaml.dump(config, f, default_flow_style=False)

print("\n\n" + "="*60)
print("Authorization Successful!")
print(f"Token saved to: {yaml_path}")
print("="*60)
