from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is online!"

def run():
    # Runs the web server
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    # Puts the web server in a background thread so the bot can boot!
    t = Thread(target=run)
    t.start()
