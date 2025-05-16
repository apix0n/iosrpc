from flask import Flask, request, jsonify
from pypresence import Presence
import time
import threading
from itunes import get_ios_app_icon
from dotenv import load_dotenv
import os

load_dotenv()

# === CONFIGURATION ===
CLIENT_ID = os.getenv("CLIENT_ID") # Replace with your Discord application's client ID
PORT = 5000  # Port for Flask server
# ======================

if CLIENT_ID is None:
    raise ValueError("CLIENT_ID not set. Please set it in your environment variables.")
# ======================

app = Flask(__name__)
rpc = None
last_request_data = {}

# Start Discord RPC in a separate thread
def start_rpc():
    global rpc
    rpc = Presence(CLIENT_ID)
    rpc.connect()
    print("Connected to Discord RPC")

def body_changed(new_data):
    global last_request_data

    return last_request_data != new_data

# Endpoint to update Rich Presence
@app.route('/update', methods=['POST'])
def update_presence():
    global rpc, last_request_data
    data = request.json
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400

    try:
        app_name = data.get("app_name", "").strip()
        bundle_id = data.get("bundle_id", "").strip()

        # Clear presence if both app_name and bundle_id are empty
        if not app_name and not bundle_id:
            rpc.clear()
            last_request_data = {}
            return jsonify({"status": "Presence cleared due to empty app_name and bundle_id."})

        if body_changed(data):
            large_image = get_ios_app_icon(bundle_id) if bundle_id else None
            start_time = None if data.get("disable_timer") else time.time()

            payload = {
                "name": app_name or "iOS App",
                "details": "Playing on iOS",
                "large_image": large_image,
                "large_text": app_name,
                "small_image": "https://avatars.githubusercontent.com/u/64981298?s=96&v=4",
                "small_text": "iosrpc by @apix0n",
                "start": start_time
            }

            rpc.update(**payload)
            last_request_data = data
            return jsonify({"status": "Presence updated."})
        else:
            return jsonify({"status": "No changes, presence not updated."})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear', methods=['POST'])
def clear_presence():
    global last_payload
    try:
        rpc.clear()
        last_payload = {}
        return jsonify({"status": "Presence cleared."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    threading.Thread(target=start_rpc, daemon=True).start()
    app.run(host='0.0.0.0', port=PORT)
