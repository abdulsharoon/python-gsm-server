from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

FIREBASE_URL = "https://modbuscapture-default-rtdb.asia-southeast1.firebasedatabase.app/deviceData.json"

@app.route("/post", methods=["POST"])
def receive_from_gsm():
    try:
        data = request.get_json(force=True)
        print("Received from GSM:", data)
        data["timestamp"] = int(time.time())
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


# 🔥 NEW TEST ENDPOINT
@app.route("/testfirebase")
def test_firebase():
    test_data = {
        "server_test": "hello_from_python_server",
        "timestamp": int(time.time())
    }
    fb = requests.post(FIREBASE_URL, json=test_data)
    return jsonify({
        "message": "Test sent to Firebase",
        "firebase_status": fb.status_code,
        "firebase_response": fb.text
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

