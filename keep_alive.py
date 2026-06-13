from flask import Flask, request, redirect
from threading import Thread
import os
import requests
import json
import shared  # Import the real-time memory bridge

app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "https://badnam-1.onrender.com/callback"
TOKENS_FILE = "oauth_tokens.json"

def save_token(user_id, access_token, refresh_token):
    if not os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, "w") as f: json.dump({}, f)
    with open(TOKENS_FILE, "r") as f:
        try: data = json.load(f)
        except json.JSONDecodeError: data = {}
    data[str(user_id)] = {"access_token": access_token, "refresh_token": refresh_token}
    with open(TOKENS_FILE, "w") as f: json.dump(data, f, indent=4)

@app.route('/')
def home(): 
    return "BADNAM Security System Online."

@app.route('/login')
def login():
    url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={requests.utils.quote(REDIRECT_URI)}&response_type=code&scope=identify%20guilds.join"
    return redirect(url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code: return "❌ Missing authorization code.", 400

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    res = requests.post("https://discord.com/api/v10/oauth2/token", data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'}).json()
    if "access_token" not in res: return "❌ Verification expired or failed.", 400

    user_info = requests.get("https://discord.com/api/v10/users/@me", headers={'Authorization': f"Bearer {res['access_token']}"}).json()
    if "id" not in user_info: return "❌ Profile read failed.", 400

    user_id = user_info['id']
    save_token(user_id, res['access_token'], res['refresh_token'])
    
    # Send directly to the bot's live memory stream
    shared.pending_users.append(str(user_id))

    return f"""
    <html><body style="background:#2b2d31;color:white;text-align:center;font-family:sans-serif;padding-top:80px;">
    <div style="background:#1e1f22;display:inline-block;padding:40px;border-radius:8px;box-shadow:0 4px 10px rgba(0,0,0,0.3);">
    <h1 style="color:#23a55a;">✅ Verified Successfully</h1>
    <p>Thank you, <b>{user_info.get('username', 'User')}</b>! Your account is safe.</p>
    <p>You can close this tab and head back to the server.</p>
    </div></body></html>
    """

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()
