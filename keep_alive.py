from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive! Monitoring system active."

def run():
    # Use 8080 as it matches your current Render log configuration
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """
    Starts the Flask server in a separate thread 
    so it doesn't block the Discord bot from starting.
    """
    t = Thread(target=run)
    t.start()
