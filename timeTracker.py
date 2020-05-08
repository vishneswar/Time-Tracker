import win32gui
import json
import time
import re
import datetime as dt
import os

def timeTracker():
	"""Tracks the time spent on windows PC and exports the data as JSON"""
	date_str = dt.datetime.today()
	date_str = dt.datetime.strftime(date_str, '%Y-%m-%d')
	tracking = get_json(date_str)
	pre_window = ''
	try:
		while True:
			current_window = get_currentWindow()
			
			if pre_window != current_window:
				date = dt.datetime.now().strftime('%Y-%m-%d')
				current_time = dt.datetime.now().strftime('%H:%M:%S')
				if pre_window:
					for items in tracking['activities']:
						if items['event'] == pre_window:
							dicc = items['log'][len(items['log']) - 1]
							dicc['end_date'] = date
							dicc['end_time'] = current_time
							dicc['duration'] = str(dt.datetime.strptime(dicc['end_time'], '%H:%M:%S') - dt.datetime.strptime(dicc['start_time'], '%H:%M:%S'))
							save_json(tracking, date)
							print(dicc['duration'])
									
		
				pre_window = current_window
				print(current_window.ljust(50), end='')
				for items in tracking['activities']:
					if items['event'] == current_window:
						dicc = {}
						dicc['start_date'] = date
						dicc['start_time'] = current_time
						items['log'].append(dicc)
						break

				else:
					dic = {}
					dic.setdefault('event', current_window) 
					dic.setdefault('log', [])
					dicc = {}
					dicc['start_date'] = date
					dicc['start_time'] = current_time
					dic['log'].append(dicc)
					tracking['activities'].append(dic)
				save_json(tracking, date)
			time.sleep(1)
			
	except KeyboardInterrupt:
		date = dt.datetime.now().strftime('%Y-%m-%d')
		current_time = dt.datetime.now().strftime('%H:%M:%S')
		if pre_window:
			for items in tracking['activities']:
				if items['event'] == pre_window:
					dicc = items['log'][len(items['log']) - 1]
					dicc['end_date'] = date
					dicc['end_time'] = current_time
					dicc['duration'] = str(dt.datetime.strptime(dicc['end_time'], '%H:%M:%S') - dt.datetime.strptime(dicc['start_time'], '%H:%M:%S'))
		save_json(tracking)
		print('\nExiting the Program...')


def save_json(tracking, date_str):
	"""Saves the json file"""
	try:
		os.makedirs(date_str)
	except FileExistsError:
		pass
	with open(os.path.join(date_str, 'timetracker.json'), 'w') as file:
			json.dump(tracking, file)
			

def get_json(date_str):
	"""Returns json if exits in the dir else creates a new json"""
	try:
		os.makedirs(date_str)
	except FileExistsError:
		print('Folder already exits')
	try:
		with open(os.path.join(date_str, 'timetracker.json'), 'r') as file:
			return json.load(file)
	except:
		return {'activities': []}

def get_currentWindow():
	"""Returns the current window"""
	window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
	if re.search('(.*cmd\.exe.*)|(.*py.exe.*)', window):
		window = 'terminal'
	elif re.search('.*- Google Chrome', window):
		window = 'Google Chrome'
	elif re.search('.* Sublime Text.*', window):
		window = 'Sublime Text'
	elif re.search('.*Visual Studio Code*', window):
		window = 'Visual Studio Code'
	elif re.search('.*Eclipse.*', window):
		window = 'Eclipse'
	elif re.search('.*Excel.*', window):
		window = 'Excel'
	elif window == '':
		window = 'Desktop'
	elif re.search('.*Notepad.*', window):
		window = 'Notepad'
	elif re.search('.*Outlook.*', window):
		window = 'Outlook'


	return window


if __name__== '__main__':
	timeTracker()