import os
import shutil
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'	#To suppress warnings thrown by tensorflow
import Detector as D
import Editor as E
import OCR
import numpy as np
import Levenshtein
import subprocess


def main(vid, video,model):

	
	frRt = int(vid.get(cv2.CAP_PROP_FPS))
	print(frRt)
	i = 0
	ht=''
	at=''
	ht_at_box = None
	log = open('events.txt', 'w')

	
	while vid.isOpened():
			ret, frame = vid.read()
			
			if not ret:
					break
			
			if i % (5 * frRt) == 0:
					cv2.imwrite('Image.png', frame)
					classes, boxes = D.detect(model,'Image.png')
					
					for name, box in zip(classes, boxes):
							if name == 'HT&AT':
									ht_at_box = box
									x1, y1, x2, y2 = map(int, box)
									cropped_image = frame[y1:y2, x1:x2]
									cv2.imwrite('crop_ht&at.jpg', cropped_image)
									ht,at=OCR.HomeTeam_awayTeam('crop_ht&at.jpg')
									ht=ht.upper()
									at=at.upper()
									print(ht,at)
									break
					if ht_at_box:
							break
			i += 1
	
	events = {
			'1': {f'Goals Scored by {ht}': 0, f'Goals Scored by {at}': 0,
				 			f'Yellow card {ht}': 0,f'Yellow card {at}':0,
							f'Red card {ht}': 0,f'Red card {at}':0,
							f'Substitution {ht}': 0,f'Substitution {at}':0,
							f'Red card':0,f'Substitution': 0,f'Yellow card': 0}
	}['1']
	frNo = 1	
	prescore = (0, 0)	
	consecutive_event_frames = 0
	while(video.isOpened()):    
		ret, frame = video.read()
		if not ret:
				break

		if frNo % frRt == 0:
				cv2.imwrite('Image.png', frame)
				classes, boxes = D.detect(model,'Image.png')	
				check=1
				ev=0
				team_name = ''
				for name, box in zip(classes, boxes):
					if name == 'NP':
							check=2
				for name, box in zip(classes, boxes):
					if name == 'Event' and check==2:
							consecutive_event_frames+=1
							for namet, _ in zip(classes, boxes):
								if namet in ['F-MUN', 'F-MCI', 'F-TOT', 'F-LIV', 'F-CRY', 'F-CHE', 'F-NEW']:
										team_name = namet[-3:]
							if consecutive_event_frames==2:
								x1, y1, x2, y2 = map(int, box)
								cropped_image = frame[y1:y2, x1:x2]
								cv2.imwrite('crop_event.jpg', cropped_image)
								event=OCR.text('crop_event.jpg')
								known_statements = ["Yellow card", "Red card", "Goal", "Substitution"]
								event = min(known_statements, key=lambda statement: Levenshtein.distance(event.lower(), statement.lower()))
								if event == 'Goal':
										print('----------------------------------------------')
										player_name = ''
										Time=''

										for name, box in zip(classes, boxes):
												if name == 'NP':
														x1, y1, x2, y2 = map(int, box)
														cropped_image = frame[y1:y2, x1:x2]
														cv2.imwrite('crop_NP.jpg', cropped_image)
														player_name=OCR.text('crop_NP.jpg')
												elif name == 'Time':
														x1, y1, x2, y2 = map(int, box)
														cropped_image = frame[y1:y2, x1:x2]
														cv2.imwrite('crop_Time.jpg', cropped_image)
														Time =OCR.text('crop_Time.jpg')
										for name, box in zip(classes, boxes):
												if name == 'SB':
														x1, y1, x2, y2 = map(int, box)
														cropped_image = frame[y1:y2, x1:x2]
														cv2.imwrite('crop_SB.jpg', cropped_image)
														score=OCR.SB('crop_SB.jpg')
														print(score)
														print(prescore)
														print(score[0],score[1],prescore[0],prescore[1])
														sec=frNo//frRt
														if score[0] == prescore[0] + 1:
																print('ht gool')
																events[f'Goals Scored by {ht}'] += 1
																timeStamps.append(sec)
																log_entry = f'{ht} {player_name} {Time} ~ {event}'
																log.write(log_entry + '\n')
																print(log_entry)
														elif score[1] == prescore[1] + 1:
																print('at gool')
																events[f'Goals Scored by {at}'] += 1
																timeStamps.append(sec)
																log_entry = f'{at} {player_name} {Time} ~ {event}'
																log.write(log_entry + '\n')
																print(log_entry)
														prescore = score
										print('----------------------------------------------')
								else :
									print('----------------------------------------------')
									player_name = ''
									Time='-:-'
									player1=''
									player2=''

									for name, box in zip(classes, boxes):
											if at=='MCI' and team_name=='CHE':
												team_name='MCI'
											if name == 'NP' and event=='Substitution':
													x1, y1, x2, y2 = map(int, box)
													cropped_image = frame[y1:y2, x1:x2]
													cv2.imwrite('crop_NP.jpg', cropped_image)
													player1,player2=OCR.Substitution('crop_NP.jpg')
											elif name == 'NP':
													x1, y1, x2, y2 = map(int, box)
													cropped_image = frame[y1:y2, x1:x2]
													cv2.imwrite('crop_NP.jpg', cropped_image)
													player_name=OCR.text('crop_NP.jpg')
											elif name == 'Time':
													x1, y1, x2, y2 = map(int, box)
													cropped_image = frame[y1:y2, x1:x2]
													cv2.imwrite('crop_Time.jpg', cropped_image)
													Time =OCR.text('crop_Time.jpg')
									if(player1==''):
										log_entry = f'{team_name} {player_name} {Time} ~ {event}'
									else:
										log_entry = f'{team_name} (player-out = {player1}) (player-in = {player2}) {Time} ~ {event}'

									log.write(log_entry + '\n')
									print(log_entry)
									if team_name == ht:
											events[f'{event} {ht}'] += 1
											events[f'{event}'] += 1
									elif team_name ==at:
											events[f'{event} {at}'] += 1
											events[f'{event}'] += 1
									else :
											events[f'{event}'] += 1
									print('----------------------------------------------')
								if consecutive_event_frames==2:
									consecutive_event_frames=-1
							ev=1
				if ev==0:
					consecutive_event_frames=0
		frNo += 1

	video.release()

	print(events)
	for i,j in events.items():
		log.write(f'\n{i}: {j}')
	log.close()

def getGame():
	vidName, extension = input('Enter Name of Video File: ').split('.')
	path = f'{os.getcwd()}/{vidName}'	
	try:	
		shutil.rmtree(path)
	except:
		pass
	finally:
		os.mkdir(path); os.chdir(path)

	try:	
		vid = cv2.VideoCapture(f'{path}.{extension}')	
		video = cv2.VideoCapture(f'{path}.{extension}')	
	except:
		input('No such file'); exit()
  
	main(vid, video,model)
	
	E.combine(extension, timeStamps, path)

if __name__ == "__main__":
	model_path = 'event.pt'
	model = D.load_model(model_path)
	timeStamps = []
	getGame()
	subprocess.run(["streamlit", "run", "../app.py"])
