from pathlib import Path
import cv2
import tensorflow as tf
import numpy as np
import time
from collections import Counter
import requests

MODEL_PATH = Path(__file__).resolve().parent / "csk_vision_model.keras"
BACKEND_URL = "http://127.0.0.1:5000/new_sign"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)

class_names = ["approved", "peace", "wave"]


def send_prediction(sign: str, confidence: float) -> None:
    payload = {
        "sign": sign,
        "confidence": f"{confidence:.1f}%",
    }
    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=2)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Failed to send prediction to backend: {exc}")


prediction_history = []
start_time = time.time()
prediction_duration = 1.0
camera = cv2.VideoCapture(0)

label = "Analyzing..."
while True:
    success, frame = camera.read()

    if not success:
        print("Could not access the webcam.")
        break

    image = cv2.resize(frame, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.expand_dims(image, axis=0)

    predictions = model.predict(image, verbose=0)
    predicted_class = np.argmax(predictions[0])
    prediction_history.append(predicted_class)

    if time.time() - start_time >= prediction_duration:
        most_common_class = Counter(prediction_history).most_common(1)[0][0]
        confidence = (
            prediction_history.count(most_common_class) / len(prediction_history)
        ) * 100

        sign = class_names[most_common_class]
        label = f"{sign}: {confidence:.1f}%"
        send_prediction(sign, confidence)

        prediction_history = []
        start_time = time.time()

    cv2.putText(
        frame,
        label,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("CSK Vision - Webcam Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()
