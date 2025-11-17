from flask import Flask
import requests
import threading
import time

app = Flask(__name__)

# 🟩 Firebase A (where GSM writes)
FIREBASE_A = "https://gsmdatatoserver-default-rtdb.asia-southeast1.firebasedatabase.app/GSM_Data.json"

# 🟦 Firebase B (your ORIGINAL project → meter_data)
FIREBASE_B = "https://modbuscapture-default-rtdb.asia-southeast1.firebasedatabase.app/meter_data.json"

last_key = None   # To detect new GSM data

def sync_loop():
    global last_key
    while True:
        try:
            # 1️⃣ Read all GSM nodes from Firebase A
            data = requests.get(FIREBASE_A).json()

            if data:
                # get the LATEST push-ID entry
                latest_key = list(data.keys())[-1]
                latest_value = data[latest_key]

                # 2️⃣ Only forward NEW data
                if latest_key != last_key:
                    print("Forwarding:", latest_value)

                    # 3️⃣ PUT into meter_data of Firebase B
                    requests.put(FIREBASE_B, json=latest_value)

                    # Save this key as last processed
                    last_key = latest_key

        except Exception as e:
            print("Sync error:", e)

        time.sleep(3)   # Check every 3 seconds


# Start sync thread
threading.Thread(target=sync_loop, daemon=True).start()

@app.route("/")
def home():
    return "Firebase A → Firebase B sync running OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
