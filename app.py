from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace
import threading
import os

app = Flask(__name__)

# Webcam (local only; Render may not use this in production)
camera = cv2.VideoCapture(0)

current_emotion = {"emotion": "detecting...", "confidence": 0}
lock = threading.Lock()


def generate_frames():
    frame_count = 0

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame_count += 1

        try:
            # Run DeepFace every 10 frames (performance fix)
            if frame_count % 10 == 0:
                result = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False
                )

                emotion = result[0]['dominant_emotion']
                confidence = round(result[0]['emotion'][emotion], 1)

                with lock:
                    current_emotion["emotion"] = emotion
                    current_emotion["confidence"] = confidence

            # Display label on video
            label = f"{current_emotion['emotion']} ({current_emotion['confidence']}%)"
            cv2.putText(frame, label, (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (200, 240, 96), 2)

        except Exception as e:
            print("Error:", e)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/emotion')
def emotion():
    with lock:
        return jsonify(current_emotion)


# ✅ IMPORTANT: Render deployment fix
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
