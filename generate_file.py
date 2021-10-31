from Crypto.Cipher import AES
from glob import glob
import pyqrcode
import argparse
import base64
import config
import random
import struct
import string
import wave
import cv2
import sys
import os
import re


temp_folder = "."

def encrypt_text(message, aes_key):
	message = message.encode()
	BS = 16
	pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
	raw = pad(message)
	cipher = AES.new(aes_key.encode("utf8"), AES.MODE_CBC, (chr(0) * 16).encode("utf8"))
	enc = cipher.encrypt(raw)
	return base64.b64encode(enc).decode('utf-8')


def generate_frames(image_type, command):
	if command is None:
		images_counter = 0
		while True:
			cmd_ = input("Enter a command or 'exit' to generate video: ")
			images_counter += 1
			if cmd_ != "exit":
				temp_image_path = temp_folder+"/image_"+str(images_counter)+".png"
				create_image(cmd_, image_type, temp_image_path)
			else:
				return images_counter
				break
	else:
		temp_image_path = temp_folder+"/image_1.png"
		create_image(command, image_type, temp_image_path)
		return 1


def create_video_file(video_file):
	img_array = []
	natsort = lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split('(\d+)', s)]
	for filename in sorted(glob(temp_folder+'/*.png'), key=natsort):
		img = cv2.imread(filename)
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		fps = 1
		out = cv2.VideoWriter(video_file,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
	for i in range(len(img_array)):
		out.write(img_array[i])
	out.release()


def clean_images(images_counter, temp_folder):
	for i in range(1, images_counter+1):
		os.remove(temp_folder + "/image_" +  str(int(i)) + ".png")


def generate_video(image_type, video_file, temp_folder, command):
	images_counter = generate_frames(image_type, command)
	create_video_file(video_file)
	clean_images(images_counter, temp_folder)


def get_text_lines():
	cmd_list = []
	while True:
		cmd_ = input("Enter a command or 'exit' to generate the text file: ")
		if cmd_ != "exit":
			cmd_list.append(cmd_)
		else:
			return cmd_list
			break


def encrypt_list(cmd_list):
	encrypted_list = []
	for cmd_ in cmd_list:
		encrypted_list.append(encrypt_text(cmd_,config.aes_key))
	return encrypted_list


def create_text_file(text_file, cmd_list):
	outfile = open(text_file, "w")
	for element in cmd_list:
		outfile.write(element + "\n")


def generate_textfile(text_type, text_file, command):
	if command is None:
		cmd_list = get_text_lines()
	else:
		cmd_list = [command]
	if text_type == "text_encrypted":
		cmd_list = encrypt_list(cmd_list)
	create_text_file(text_file, cmd_list)


def create_image(cmd_, image_type, image_file):
	if image_type == "qr":
		qrcode = pyqrcode.create(cmd_,version=10)
		qrcode.png(image_file,scale=8)
	elif image_type == "qr_aes":
		encrypted_cmd = encrypt_text(cmd_,config.aes_key)
		qrcode = pyqrcode.create(encrypted_cmd,version=10)
		qrcode.png(image_file,scale=8)
	else:
		print("[-] Unexpected image type :(")


def generate_image(image_type, image_file, command):
	if command is None:
		cmd_ = input("Enter a command: ")
	else:
		cmd_ = command
	create_image(cmd_, image_type, image_file)


def ascii_to_binary(ascii_value):
    all_str = ''.join([str(bin(ord(i))[2:]).zfill(7) for i in ascii_value])
    return [int(c) for c in all_str]


def create_wav(binary_list, path):
    noise_output = wave.open(path, 'w')
    noise_output.setparams((1, 2, 44100, 0, 'NONE', 'not compressed'))
    values = []
    for i in binary_list:
    	packed_value = struct.pack('h', i)
    	values.append(packed_value)
    value_str = b"".join(values)
    noise_output.writeframes(value_str)
    noise_output.close()


def generate_audio(file_type, outputfile, command):
	if file_type == "audio_encrypted":
		command = encrypt_text(command, config.aes_key)
	binary_list = ascii_to_binary(command)
	create_wav(binary_list, outputfile)
	

def test():
	generate_textfile("text", "test1.txt", "whoami")
	generate_textfile("text_encrypted", "test2.txt", "whoami")
	generate_video("qr", "test3.avi", temp_folder, "whoami")
	generate_video("qr_aes", "test4.avi", temp_folder, "whoami")
	generate_image("qr","test5.png", "whoami")
	generate_image("qr_aes","test6.png", "whoami")
	generate_audio("audio","test7.wav", "whoami")
	generate_audio("audio_encrypted","test8.wav", "whoami")


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-t', '--type', required=True, default=None, action='store', help='Type of file: "video", "image" or "text".')
	parser.add_argument('-o', '--outputfile', required=False, default=None, action='store', help='Output file, with extensions: ".avi" for video, ".png" for image or ".txt" for text files.')
	parser.add_argument('-c', '--command', required=False, default=None, action='store', help='Command to execute.')
	parser.add_argument('-e', '--encrypted', required=False, default=False, action='store_true', help='Add this flag to encrypt the command with AES.')
	return parser


def change_aes_key():
	print("[+] Creating new AES key")
	config_lines = open("config.py").read().splitlines()
	new_config_lines = []
	for l in config_lines:
		if not "aes_key" in l:
			new_config_lines.append(l)
		else:
			new_aes_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
			new_config_lines.append("aes_key = \""+new_aes_key+"\"")
	with open("config.py", "w") as outfile:
		outfile.write("\n".join(new_config_lines))
	print("[+] New AES key: %s. Please run the program again :)"%(new_aes_key))
	sys.exit(0)


def main():
	args = get_args().parse_args()
	file_type = args.type
	encrypted = args.encrypted
	outputfile = args.outputfile
	command = args.command
	if encrypted:
		file_type += "_encrypted"
		if config.aes_key == "covert-control21":
			change_key = input("[-] Using default AES key 'covert-control21', would you like to generate a random key? [Y/n]")
			if change_key.lower() == "y" or change_key.lower() == "yes":
				change_aes_key()
	if file_type == "text" or file_type == "text_encrypted":
		if outputfile is None:
			outputfile = "test.txt"
		if not outputfile.endswith(".txt"):
			print("[-] Unexpected extension, it should be .txt")
		generate_textfile(file_type, outputfile, command)
	elif file_type == "image":
		if outputfile is None:
			outputfile = "test.png"
		if not outputfile.endswith(".png"):
			print("[-] Unexpected extension, it should be .png")
		generate_image("qr", outputfile, command)
	elif file_type == "image_encrypted":
		if outputfile is None:
			outputfile = "test.png"
		if not outputfile.endswith(".png"):
			print("[-] Unexpected extension, it should be .png")
		generate_image("qr_aes", outputfile, command)
	elif file_type == "video":
		if outputfile is None:
			outputfile = "test.avi"
		if not outputfile.endswith(".avi"):
			print("[-] Unexpected extension, it should be .avi")
		generate_video("qr", outputfile, temp_folder, command)
	elif file_type == "video_encrypted":
		if outputfile is None:
			outputfile = "test.avi"
		if not outputfile.endswith(".avi"):
			print("[-] Unexpected extension, it should be .avi")
		generate_video("qr_aes", outputfile, temp_folder, command)
	elif file_type == "audio" or file_type == "audio_encrypted":
		if outputfile is None:
			outputfile = "test.wav"
		if not outputfile.endswith(".wav"):
			print("[-] Unexpected extension, it should be .wav")
		generate_audio(file_type, outputfile, command)
	else:
		print("[-] Unexpected file type :(")


if __name__== "__main__":
	main()