import cv2
import face_recon
import logging
from face_recon_utilities import get_logger

logger = get_logger()

def main():
	logger.debug("Running Main...")
	exit_status = face_recon.main()

if __name__ == "__main__":
	main()

#main()
# # Assuming the range of motion for pan is from -90 to +90 degrees
# pan_min = -90
# pan_max = 90

# # Assuming the range of motion for tilt is from -45 to +45 degrees
# tilt_min = -45
# tilt_max = 45

# RETRY_COUNT_ON_FAILED_FRAME_CAPTURE = 5
# retry_count = 0


# # Load the pre-trained face cascade classifier
# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# # Initialize the video capture object
# video_capture = cv2.VideoCapture(0)  # Use 0 for the default camera

# while True:
#     # Read a single frame from the video capture
#     ret, frame = video_capture.read()
	
#     if not ret:
#         if retry_count < RETRY_COUNT_ON_FAILED_FRAME_CAPTURE:
#             retry_count += 1
#             continue
#        	else:
#             break

#     retry_count = 0

#     # Convert the frame to grayscale for face detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
#     # Detect faces in the frame
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
	
#     # Iterate over each detected face
#     for (x, y, w, h) in faces:
#         # Calculate the central coordinates of the face
#         center_x = x + w // 2
#         center_y = y + h // 2
		
#         # Convert the central coordinates to gimbal inputs
#         pan_input = ((center_x / frame_width) * (pan_max - pan_min)) + pan_min
#         tilt_input = ((center_y / frame_height) * (tilt_max - tilt_min)) + tilt_min
		
#         # Draw a rectangle around the face
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
#         # Draw a circle at the central coordinates of the face
#         cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), 2)
		
#         # Display the central coordinates on the frame
#         cv2.putText(frame, f"({center_x}, {center_y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
	
#     # Display the resulting frame
#     cv2.imshow('Face Detection', frame)
	
#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the video capture object and close all windows
# video_capture.release()
# cv2.destroyAllWindows()