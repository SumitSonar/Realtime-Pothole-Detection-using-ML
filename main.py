import cv2
import numpy as np
from ultralytics import YOLO
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# import logging
import requests
# Initialize logging
# logging.basicConfig(level=logging.INFO)

# Load the YOLOv8 model
model_path = 'y8best.pt'  # Change this to your desired model
model = YOLO(model_path)

# Path to your static video file
# VIDEO_PATH = 'static/p.mp4'  # Update the path to your video file
ESP32_CAM_URL = "http://192.168.183.120/"
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Global variable to track pothole detection status
pothole_detected = False


def gen_frames():
    global pothole_detected
    byte_buffer = b''

    try:
        # Make a request to the ESP32-CAM stream
        stream = requests.get(ESP32_CAM_URL, stream=True)

        if stream.status_code != 200:
            
            return

        for chunk in stream.iter_content(chunk_size=1024):
            byte_buffer += chunk
            a = byte_buffer.find(b'\xff\xd8')  # JPEG start
            b = byte_buffer.find(b'\xff\xd9')  # JPEG end

            if a != -1 and b != -1:
                # Extract the JPEG image and reset the buffer
                jpg = byte_buffer[a:b + 2]
                byte_buffer = byte_buffer[b + 2:]

                # Decode the frame from JPEG
                frame = cv2.imdecode(np.frombuffer(
                    jpg, np.uint8), cv2.IMREAD_COLOR)

                if frame is None:
                    # logging.warning("Failed to decode frame.")
                    continue

                # Perform YOLOv8 inference
                results = model(frame)
                pothole_detected = False  # Reset detection status for each frame

                # Loop over the detections and check for potholes
                for result in results:
                    boxes = result.boxes  # YOLOv8 boxes object
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = box.conf[0]  # Confidence of the detection
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        # Check if the detected object is a pothole
                        label = model.names[cls]
                        if label !=None:  # Confidence threshold
                            pothole_detected = True

                            # Draw a rectangular bounding box around the pothole
                            cv2.rectangle(frame, (x1, y1), (x2, y2),
                                          (0, 0, 255), 2)  # Red rectangle
                            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)  # Red text

                            # Optionally, draw a circle at the center of the pothole for emphasis
                            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
                            cv2.circle(frame, (center_x, center_y),
                                       5, (0, 255, 0), -1)  # Green circle

                # Encode the frame with bounding boxes to JPEG
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    # logging.warning("Failed to encode frame.")
                    continue

                frame = buffer.tobytes()

                # Yield the frame as part of the video stream response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except requests.exceptions.RequestException as e:
        print(f"Error with ESP32-CAM stream: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


@app.get("/")
async def index(request: Request):
    """Render the home page with a video feed."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about")
async def about(request: Request):
    """Render the about page."""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/dashboard")
async def dashboard(request: Request):
    """Render the dashboard page."""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/video_feed")
async def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return StreamingResponse(gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get("/pothole_detection_status")
async def pothole_detection_status():
    """Return the pothole detection status as JSON."""
    global pothole_detected
    return JSONResponse({'pothole_detected': pothole_detected})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
