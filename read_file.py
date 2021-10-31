from pyzbar.pyzbar import decode
from Crypto.Cipher import AES
from PIL import Image
from glob import glob
import datetime
import base64
import config
import random
import struct
import wave
import cv2
import re
import os


def get_frames(video_path, imagesFolder):
	cap = cv2.VideoCapture(video_path)
	frameRate = int(cap.get(cv2.CAP_PROP_FPS))
	images_counter = 0
	while(cap.isOpened()):
		frameId = cap.get(1)
		ret, frame = cap.read()
		if (ret != True):
			break
		if (frameId % frameRate == 0):
			images_counter += 1
			filename = imagesFolder + "/image_" +  str(int(images_counter)) + ".png"
			height, width, layers = frame.shape
			size = (width,height)
			cv2.imwrite(filename, frame)
	cap.release()
	return images_counter


def read_frames(image_type, imagesFolder):
	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
	commands = []
	for filename in sorted(glob(imagesFolder+'/*.png'), key=natsort):
		if image_type == "qr":
			text = decode(Image.open(filename))[0].data.decode()
		elif image_type == "qr_aes":
			encrypted_text = decode(Image.open(filename))[0].data.decode()
			text = decrypt_text(encrypted_text)
		else:
			print("[-] Error: Unknown type")
			return "unknown_type"
		commands.append(text)
	return commands


def clean_images(images_counter, imagesFolder):
	for i in range(1, images_counter+1):
		os.remove(imagesFolder + "/image_" +  str(int(i)) + ".png")


def read_video(image_type, video_path, imagesFolder):
	images_counter = get_frames(video_path, imagesFolder)
	commands = read_frames(image_type, imagesFolder)
	clean_images(images_counter, imagesFolder)
	return commands


def decrypt_text(encrypted_text):
	try:
		enc = base64.b64decode(encrypted_text)
		cipher = AES.new(config.aes_key.encode("utf-8"), AES.MODE_CBC, (chr(0) * 16).encode("utf-8")) # yes, IV is all zeros xD
		dec = cipher.decrypt(enc)
		unpad = lambda s: s[:-ord(s[len(s)-1:])]
		return unpad(dec).decode('utf-8')
	except:
		now = datetime.datetime.now()
		if config.debug: print("[%02d:%02d:%02d] AES decryption was unsuccessful. Maybe you uploaded an unecrypted file?"%(now.hour,now.minute,now.second))
		return ""


def get_text(text_path):
	return open(text_path).read().splitlines()


def decrypt_list(encrypted_list):
	decrypted_list = []
	for encrypted_text in encrypted_list:
		decrypted_list.append(decrypt_text(encrypted_text))
	return decrypted_list


def read_text(text_type, text_path):
	commands = ""
	if text_type == "text":
		commands = get_text(text_path)
	elif text_type == "text_encrypted":
		encrypted_commands = get_text(text_path)
		commands = decrypt_list(encrypted_commands)
	return commands


def read_image(image_type, image_path):
	text = decode(Image.open(image_path))[0].data.decode()
	if image_type == "qr":
		return [text]
	elif image_type == "qr_aes":
		return [decrypt_text(text)]


def binary_to_ascii(binary_list):
    all_str = ''.join([str(i) for i in binary_list])
    return ''.join([chr(int(all_str[i:i+7],2)) for i in range(0, len(all_str), 7)])


def process_wav(path):
    with wave.open(path, "rb") as wav:
        nchannels, sampwidth, framerate, nframes, _, _ = wav.getparams()
        all_bytes = wav.readframes(-1)
    framewidth = sampwidth * nchannels
    frames = (all_bytes[i * framewidth: (i + 1) * framewidth]  for i in range(nframes))
    binary_output = []
    for frame in frames:
        binary_val = struct.unpack('h',frame)[0]
        binary_output.append(binary_val)
    return binary_output


def read_audio(audio_type, audio_path):
	binary_output = process_wav(audio_path)
	result_ascii_value = binary_to_ascii(binary_output)
	if audio_type == "audio_encrypted":
		result_ascii_value = decrypt_text(result_ascii_value)
	return [result_ascii_value]


def main():
	print(read_text("text", "test1.txt"))
	print(read_text("text_encrypted", "test2.txt"))
	print(read_video("qr", "test3.avi", "."))
	print(read_video("qr_aes", "test4.avi", "."))
	print(read_image("qr", "test5.png"))
	print(read_image("qr_aes", "test6.png"))
	print(read_audio("audio","test7.wav"))
	print(read_audio("audio_encrypted","test8.wav"))
	

if __name__== "__main__":
	main()