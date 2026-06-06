# Emotion Detector

A real-time facial emotion detection web application built with Flask, OpenCV, and DeepFace.

## Features

* Live webcam feed
* Real-time emotion recognition
* Confidence percentage display
* Web-based interface
* JSON API endpoint for emotion data

## Technologies Used

* Python
* Flask
* OpenCV
* DeepFace
* TensorFlow
* NumPy

## Project Structure

```text
emotion_detector/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/alexdavidovmain/emotion-detector.git
cd emotion-detector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open in Browser

Visit:

```text
http://127.0.0.1:5000
```

## API Endpoints

### Home Page

```http
GET /
```

Displays the emotion detection interface.

### Video Stream

```http
GET /video
```

Returns the live webcam stream.

### Current Emotion

```http
GET /emotion
```

Example Response:

```json
{
  "emotion": "happy",
  "confidence": 97.4
}
```

## How It Works

1. OpenCV captures frames from the webcam.
2. DeepFace analyzes each frame for facial emotions.
3. The dominant emotion and confidence score are calculated.
4. Results are displayed on the video feed in real time.
5. Current emotion data is exposed through a JSON endpoint.

## Requirements

* Python 3.10+
* Webcam
* Internet connection (for initial package installation)

## Disclaimer

Emotion recognition models are not always accurate and results may vary depending on lighting conditions, camera quality, facial visibility, and model limitations.

## License

This project is provided for educational and personal use.


Made by Alexander Davidov
