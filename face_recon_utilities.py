import queue
import logging

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logger = logging.getLogger(__name__)
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

def get_logger():
	return logger

def handle_angles(angle_queue):
	while True:
		try:
			pan_input, tilt_input = angle_queue.get()

			# send these to the arduino
			print(pan_input)
			print(tilt_input)
		except queue.Empty:
			# Lets avoid high CPU usage
			time.sleep(0.1)