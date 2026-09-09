from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

sign = "Initialising..."
confidence = "0%"


@app.route("/")
def home():
    return render_template("index.html", sign=sign, confidence=confidence)


@app.route("/get_sign")
def get_sign():
    return jsonify({"sign": sign, "confidence": confidence})


@app.route("/new_sign", methods=["POST"])
def new_sign():
    global sign, confidence

    data = request.get_json(silent=True) or {}
    sign = data.get("sign", sign)
    confidence = data.get("confidence", confidence)

    return jsonify({"status": "ok", "sign": sign, "confidence": confidence})


if __name__ == "__main__":
    app.run(debug=True)