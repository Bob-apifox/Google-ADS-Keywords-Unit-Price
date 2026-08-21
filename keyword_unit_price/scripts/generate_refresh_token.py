import os
import yaml
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

YAML_PATH = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'

def main():
    # 1. Read existing client credentials
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
    
    print("\n" + "="*70)
    print("Opening browser for Google Account Authorization...")
    print("If the browser doesn't open automatically, please copy the URL below into your browser manually!")
    print("="*70 + "\n")
    
    # Run the local server to handle the OAuth2 callback
    credentials = flow.run_local_server(port=0)
    
    new_refresh_token = credentials.refresh_token
    
    if new_refresh_token:
        # 3. Update the YAML file automatically
        config['refresh_token'] = new_refresh_token
        with open(YAML_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"\n[SUCCESS] Successfully acquired new Refresh Token: {new_refresh_token[:15]}...")
        print("[SUCCESS] google-ads.yaml has been automatically updated!")
        print("\nYou can now run the expansion scripts.")
    else:
        print("\n[ERROR] Failed to get Refresh Token. You might have authorized it already.")
        print("[TIP] Go to your Google Account security settings (https://myaccount.google.com/connections), revoke the app access, and run this script again.")

if __name__ == "__main__":
    main()
