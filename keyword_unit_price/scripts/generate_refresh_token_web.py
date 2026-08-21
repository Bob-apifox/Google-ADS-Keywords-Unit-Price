import os
import sys
import yaml
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

YAML_PATH = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    with open(YAML_PATH, 'r') as f:
        config = yaml.safe_load(f)
        
    client_id = config.get('client_id')
    client_secret = config.get('client_secret')
    
    if not client_id or not client_secret:
        print("Error: client_id or client_secret missing in google-ads.yaml")
        return

    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    
    scopes = ["https://www.googleapis.com/auth/adwords"]
    flow = InstalledAppFlow.from_client_config(client_config, scopes)
    flow.redirect_uri = "http://localhost:8085/"

    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    print("\n" + "="*70)
    print("AUTHORIZATION URL:")
    print(auth_url)
    print("="*70 + "\n")
    
    # Force open browser on Windows shell
    try:
        os.startfile(auth_url)
    except Exception:
        webbrowser.open(auth_url)

    # Listen on port 8085
    credentials = flow.run_local_server(port=8085, prompt='consent', access_type='offline')
    new_refresh_token = credentials.refresh_token
    
    if new_refresh_token:
        config['refresh_token'] = new_refresh_token
        with open(YAML_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"\n[SUCCESS] acquired new Refresh Token: {new_refresh_token[:15]}...")
        print("[SUCCESS] google-ads.yaml updated successfully!")
    else:
        print("\n[ERROR] Failed to get Refresh Token.")

if __name__ == "__main__":
    main()
