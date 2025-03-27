import os
from flask import Flask, Response
import cv2
import socket

app = Flask(__name__)

def generate_frames():
    camera_index = int(os.getenv("CAMERA_INDEX", 0))  # Default to camera index 0
    camera = cv2.VideoCapture(camera_index)  # Open the specified camera
    if not camera.isOpened():
        raise RuntimeError(f"Could not start camera at index {camera_index}. Please check the camera connection or index.")
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame in JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield the frame as part of a multipart response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # Route to stream the video
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    host_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server is running. Access the video feed at http://{host_ip}:5000/video_feed")
    app.run(host='0.0.0.0', port=5000, debug=True)
