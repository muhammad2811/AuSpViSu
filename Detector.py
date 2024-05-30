from imageai.Detection.Custom import CustomObjectDetection
import os


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
modelPath = os.getcwd()


def load(game):
	'''Loading the appropriate model files'''

	if game == '1':	#Football
		detector.setModelPath(f'{modelPath}/goals.h5') 
		detector.setJsonPath(f'{modelPath}/detection_config.json')
	detector.loadModel()


def detect():
	'''Detecting the scoreboard in the image and returning its location'''

	detections = detector.detectObjectsFromImage(input_image='Image.png', output_image_path='DetectedImage.png')
	for detection in detections:

		return detection['box_points']
