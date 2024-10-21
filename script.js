let videoElement = document.getElementById("liveCamera");
let canvasElement = document.getElementById("canvasOutput");
let canvasContext = canvasElement.getContext("2d");
let alertSound = document.getElementById("alertSound"); // Get the audio element

// Variable to track whether sound has already been played
let soundPlayed = false;

// Function to run when OpenCV is ready
// Wait until OpenCV.js is ready
function openCvReady() {
  console.log("OpenCV.js is ready to use.");

  // Start video stream from the ESP32-CAM
  let video = document.getElementById("liveCamera");
  let canvas = document.getElementById("canvasOutput");
  let context = canvas.getContext("2d");

  // Set the video stream source from the ESP32-CAM
  video.src = "p.mp4"; // Replace with your ESP32-CAM stream URL

  // Wait for the video to load before processing frames
  video.addEventListener("loadeddata", (event) => {
    console.log("Video stream loaded and ready.");

    // Start processing frames every 100ms once video is ready
    setInterval(() => {
      try {
        // Ensure the video is ready to be drawn on the canvas
        if (video.readyState === video.HAVE_ENOUGH_DATA) {
          // Draw the current frame from the video on the canvas
          context.drawImage(video, 0, 0, canvas.width, canvas.height);

          // Process each frame with OpenCV.js
          let imgData = context.getImageData(0, 0, canvas.width, canvas.height);
          let src = cv.matFromImageData(imgData);
          let gray = new cv.Mat();

          // Convert to grayscale
          cv.cvtColor(src, gray, cv.COLOR_RGBA2GRAY);
          // You can continue your OpenCV.js logic here for detection...

          // Release the matrices to free memory
          src.delete();
          gray.delete();
        }
      } catch (error) {
        console.error("Error processing frame: ", error);
      }
    }, 100); // Process frames every 100ms
  });

  // Error handling for video stream load failure
  video.addEventListener("error", (event) => {
    console.error("Error loading video stream", event);
    alert(
      "Failed to load the video stream. Please check the ESP32-CAM connection."
    );
  });
}

// Function to start detecting potholes
function startDetection() {
  // Set interval for processing frames every 100ms
  setInterval(processFrame, 100);
}

// Function to process the frame
function processFrame() {
  // Draw the current frame from the video on the canvas
  canvasContext.drawImage(
    videoElement,
    0,
    0,
    canvasElement.width,
    canvasElement.height
  );

  // Get the image data from the canvas
  let imgData = canvasContext.getImageData(
    0,
    0,
    canvasElement.width,
    canvasElement.height
  );
  let src = cv.matFromImageData(imgData);
  let dst = new cv.Mat();

  // Convert to grayscale
  cv.cvtColor(src, src, cv.COLOR_RGBA2GRAY);

  // Apply Gaussian blur
  cv.GaussianBlur(src, src, new cv.Size(5, 5), 0);

  // Edge detection
  cv.Canny(src, dst, 100, 200);

  // Find contours
  let contours = new cv.MatVector();
  let hierarchy = new cv.Mat();
  cv.findContours(
    dst,
    contours,
    hierarchy,
    cv.RETR_CCOMP,
    cv.CHAIN_APPROX_SIMPLE
  );

  let potholeDetected = false;

  // Draw contours and detect potholes based on contour area
  for (let i = 0; i < contours.size(); i++) {
    let area = cv.contourArea(contours.get(i));
    if (area > 1000) {
      // You can adjust the area threshold for pothole detection
      potholeDetected = true;
      // Draw the contour
      cv.drawContours(src, contours, i, new cv.Scalar(255, 0, 0), 2);
    }
  }

  // Show the processed image in the canvas
  canvasContext.putImageData(
    new ImageData(new Uint8ClampedArray(src.data), src.cols, src.rows),
    0,
    0
  );

  // Update the result message
  let resultElement = document.getElementById("result");
  resultElement.innerText = potholeDetected
    ? "Pothole detected!"
    : "No potholes detected.";

  // Play sound if pothole is detected and sound has not been played yet
  if (potholeDetected && !soundPlayed) {
    alertSound.play(); // Play the alert sound
    soundPlayed = true; // Set flag to true so sound doesn't play repeatedly
  } else if (!potholeDetected) {
    soundPlayed = false; // Reset the flag when no pothole is detected
  }

  // Release memory
  src.delete();
  dst.delete();
  contours.delete();
  hierarchy.delete();
}

// Start OpenCV.js
cv.onRuntimeInitialized = openCvReady;
