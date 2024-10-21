# Real-Time Pothole Detection and Alert System

This project focuses on developing a Real-Time Pothole Detection System that identifies potholes on roads using a combination of OpenCV, a custom ML model along with YOLOv8, and NodeMCU for real-time processing. The system detects potholes from video streams captured by an ESP32-CAM and triggers voice alerts to notify drivers.

### *Project Overview*

The goal of this project is to build an efficient and lightweight system that uses machine learning to identify potholes from live video feeds. The system uses OpenCV for image processing, and a custom-trained YOLOv8 model is integrated for enhanced pothole detection. The NodeMCU handles the real-time processing and sends alerts in case potholes are detected, with an option to integrate this information into a web interface.

### *Key Features*

-> Real-Time Pothole Detection: Detect potholes from live video streams using a custom-trained YOLOv8 model integrated with OpenCV for image pre-processing.

-> Voice Alerts: The system provides voice-based warnings when potholes are detected.

-> IoT Integration with NodeMCU: Utilizes the NodeMCU to handle video feed and control real-time notifications and alerts.

-> Web Interface: Real-time detection results are displayed on a simple web interface.

-> Cloud Independence: The system operates without cloud dependence, ensuring low latency and cost efficiency.

### *Technology Stack*

-> OpenCV: Used for real-time video capture and image pre-processing.

-> Machine Learning:

    Custom-trained model based on YOLOv8 for high-accuracy pothole detection.
    
    TensorFlow or PyTorch as the base framework for model training.
    
-> IoT Components:

    ESP32-CAM for live video capture.
    
    NodeMCU for managing the video stream and processing.
    
-> Backend:

    Node.js to handle communication between components and serve the web interface.

    Python for handling the detection and running the machine learning models.
    
-> Frontend: A simple web interface using Flask or Express.js to display detection results in real-time.

-> Voice Alert System: Integrated audio alerts triggered when a pothole is detected.

### *Future Enhancements*

-> Advanced Notifications: Add SMS or app notifications to inform drivers or relevant authorities.

-> GPS Integration: Log detected pothole locations using GPS data and create a pothole map.

-> Mobile Application: Develop a mobile app to complement the web interface.

### *Contact*

For any questions or feedback, please reach out to:

Sumit Sonar: csesumit13@gmail.com
