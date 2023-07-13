import cv2
from face_recon_utilities import handle_angles, get_logger
import queue, logging, threading

# Can maybe make a class out of this...

# Constants
# Assuming the range of motion for pan is from -90 to +90 degrees
pan_min = -90
pan_max = 90

# Assuming the range of motion for tilt is from -45 to +45 degrees
tilt_min = -45
tilt_max = 45

# Dimensions of the video frame
frame_width = None
frame_height = None

# Queue
angle_queue = None

# video capture
video_capture = None

# logger
logger = get_logger()

def setup_threading():
	logger.debug("Started Facial Recognition Threading Setup...")

	global angle_queue 
	angle_queue = queue.Queue()
	worker_thread = threading.Thread(target=handle_angles, args=(angle_queue,))
	worker_thread.start()
	return worker_thread

def dispose():
	video_capture.release()
	cv2.destroyAllWindows()
	# maybe close arduino connection heree

def run_facial_recognition():
	logger.debug("Started Facial Recognition Loop...")

	ret_val = True


	# Load the pre-trained face cascade classifier
	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

	# Initialize the video capture object
	# Should be moved to a setup function...
	global video_capture
	qqqqq = cv2.VideoCapture(0)  # Use 0 for the default camera
	frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
	frame_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

	while True:
		# Read a single frame from the video capture
		ret, frame = video_capture.read()
		
		if not ret:
			ret_val = False
			break

		# Convert the frame to grayscale for face detection
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		# Detect faces in the frame
		faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
		
		# Iterate over each detected face
		for (x, y, w, h) in faces:
			# Calculate the central coordinates of the face
			center_x = x + w // 2
			center_y = y + h // 2
			
			# Convert the central coordinates to gimbal inputs
			pan_input = ((center_x / frame_width) * (pan_max - pan_min)) + pan_min
			tilt_input = ((center_y / frame_height) * (tilt_max - tilt_min)) + tilt_min

			# Send these pan and tilt angles to arduino connected to the gimbles...
			try:
				angle_queue.put((pan_input, tilt_input))
			except:
				logger.exception("Exception in angle_queue put...")

			# Draw a rectangle around the face
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
			# Draw a circle at the central coordinates of the face
			cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), 2)
			
			# Display the central coordinates on the frame
			cv2.putText(frame, f"({center_x}, {center_y})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
		
		# Display the resulting frame
		cv2.imshow('Face Detection', frame)
		
		# Break the loop if 'q' is pressed
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# Release the video capture object and close all windows
	video_capture.release()
	cv2.destroyAllWindows()

	return ret_val

def main():
	logger.debug("Running Main...")
	worker_thread = setup_threading()

	face_recon_status = run_facial_recognition()
	face_recon_dispose = dispose()

	worker_thread.join()

	return face_recon_status and face_recon_dispose
