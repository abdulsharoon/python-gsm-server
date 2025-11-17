from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Your Firebase URL
FIREBASE_URL = "https://modbuscapture-default-rtdb.asia-southeast1.firebasedatabase.app/deviceData.json"

@app.route("/post", methods=["POST"])
def receive_from_gsm():
    try:
        data = request.get_json(force=True)
        print("Received from GSM:", data)

        # Add timestamp
        data["timestamp"] = int(time.time())

        # Forward to Firebase
        fb = requests.post(FIREBASE_URL, json=data)
        
        return jsonify({
            "status": "ok",
            "firebase_status": fb.status_code,
            "firebase_response": fb.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Python GSM Server Running OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
