from flask import Flask, request, redirect
from threading import Thread
import os
import requests
import json

app = Flask(__name__)

# Load configurations from Render Environment variables
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
BOT_TOKEN = os.environ.get("BOT_TOKEN") # Added for instant role assignment
REDIRECT_URI = "https://badnam-1.onrender.com/callback"

TOKENS_FILE = "oauth_tokens.json"
CONFIG_FILE = "recovery_config.json"

def save_token(user_id, access_token, refresh_token):
    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "w") as f: json.dump({}, f)
            
    with open(TOKENS_FILE, "r") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: data = {}
            
    data[str(user_id)] = {"access_token": access_token, "refresh_token": refresh_token}
    
    with open(TOKENS_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "BADNAM Security System Online."

@app.route('/login')
def login():
    discord_oauth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={requests.utils.quote(REDIRECT_URI)}"
        f"&response_type=code"
        f"&scope=identify%20guilds.join"
    )
    return redirect(discord_oauth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "❌ Verification failed: Missing authorization code.", 400

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    token_response = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers=headers)
    token_data = token_response.json()
    
    if "access_token" not in token_data:
        return f"❌ OAuth2 Error: {token_data.get('error_description', 'Failed to retrieve access token.')}", 400

    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']

    user_headers = {'Authorization': f'Bearer {access_token}'}
    user_response = requests.get("https://discord.com/api/v10/users/@me", headers=user_headers)
    user_info = user_response.json()

    if "id" not in user_info: return "❌ Error: Could not retrieve user profile identifier.", 400

    user_id = user_info['id']
    username = user_info.get('username', 'User')

    # 1. Save to backup database
    save_token(user_id, access_token, refresh_token)

    # 2. INSTANTLY ASSIGN THE ROLE VIA DISCORD API
    try:
        if os.path.exists(CONFIG_FILE) and BOT_TOKEN:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            
            for guild_id_str, cfg in config.items():
                role_id = cfg.get("verify_role")
                if role_id:
                    api_url = f"https://discord.com/api/v10/guilds/{guild_id_str}/members/{user_id}/roles/{role_id}"
                    # Tells Discord directly to add the role right now
                    requests.put(api_url, headers={"Authorization": f"Bot {BOT_TOKEN}"})
    except Exception as e:
        print("Instant role error:", e)

    # Return success screen
    return f"""
    <html>
        <head>
            <title>Verification Successful</title>
            <style>
                body {{ font-family: sans-serif; background-color: #2b2d31; color: white; text-align: center; padding-top: 50px; }}
                .container {{ background: #1e1f22; display: inline-block; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
                h1 {{ color: #23a55a; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ Verified Successfully</h1>
                <p>Thank you, <b>{username}</b>! Your account has been securely verified.</p>
                <p>You can now close this tab and return to Discord.</p>
            </div>
        </body>
    </html>
    """

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
