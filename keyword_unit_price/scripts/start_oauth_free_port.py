import os
import sys
import yaml
import socket
from google_auth_oauthlib.flow import InstalledAppFlow

os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'

YAML_PATH = 'd:/Apidog Work/Google ADS Keywords Unit Price/common/config/google-ads.yaml'

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

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

    free_port = find_free_port()
    flow.redirect_uri = f"http://localhost:{free_port}/"

    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')

    print(f"=== OAUTH_PORT: {free_port} ===")
    print("URL_START")
    print(auth_url)
    print("URL_END")

    with open("d:/Apidog Work/Google ADS Keywords Unit Price/common/config/auth_url.txt", "w", encoding="utf-8") as f:
        f.write(auth_url)

    credentials = flow.run_local_server(port=free_port, prompt='consent', access_type='offline')

    new_refresh_token = credentials.refresh_token
    if new_refresh_token:
        config['refresh_token'] = new_refresh_token
        with open(YAML_PATH, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"[SUCCESS] New refresh token saved to google-ads.yaml: {new_refresh_token[:15]}...")
    else:
        print("[ERROR] Refresh token missing.")

if __name__ == "__main__":
    main()
