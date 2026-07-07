from flask import Flask, render_template, Response, jsonify
import cv2
from deepface import DeepFace
import threading

app = Flask(__name__)

camera = cv2.VideoCapture(0)
current_emotion = {"emotion": "detecting...", "confidence": 0}
lock = threading.Lock()

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
            confidence = round(result[0]['emotion'][emotion], 1)
            with lock:
                current_emotion["emotion"] = emotion
                current_emotion["confidence"] = confidence
            label = f"{emotion} ({confidence}%)"
            cv2.putText(frame, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (200, 240, 96), 2)
        except:
            pass
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emotion')
def emotion():
    with lock:
        return jsonify(current_emotion)

if __name__ == '__main__':
    app.run(debug=False)
