# covert-control

Control systems remotely by uploading files to Google Drive, OneDrive, Youtube and Telegram using Python to create the files and the listeners. It allows to create text files, images, audio or videos, with the commands in cleartext or encrypted using AES.


- covert-googledrive.py - Control systems uploading files to a public folder in Google Drive.

- covert-onedrive.py - Control systems uploading files to a public folder in OneDrive.

- covert-telegram.py - Control systems with a Telegram bot.

- covert-youtube - Control systems uploading videos to Youtube (updated from [covert-tube](https://github.com/ricardojoserf/covert-tube)).


### Create files to upload

You can find example files in the folder [test_files](https://github.com/ricardojoserf/covert-control/tree/reduced/test_files) or create new ones with generate_file.py:

```
python3 generate_file.py -t TYPE [-o OUTPUTFILE] [-c COMMAND] [-e]
```
- -t (--type) [Required]: Types of file: "text", "image", "audio" or "video".

- -o (--outputfile) [Optional]: Output file, with extension ".txt" for "text", ".png" for "image", ".wav" for "audio" and ".avi" for "video".

- -c (--command) [Optional]: Command to execute.

- -e (--encrypted) [Optional]: Add this flag to encrypt the command with AES.


Examples:

```
python3 generate_file.py -t text -c "whoami" -o text.txt
python3 generate_file.py -t text -c "whoami" -o text_encrypted.txt -e
python3 generate_file.py -t audio -c "whoami" -o audio.wav
python3 generate_file.py -t audio -c "whoami" -o audio_encrypted.wav -e
python3 generate_file.py -t image -c "whoami" -o image.png
python3 generate_file.py -t image -c "whoami" -o image_encrypted.png -e
python3 generate_file.py -t video -c "whoami" -o video.avi
python3 generate_file.py -t video -c "whoami" -o video_encrypted.avi -e
```


### Common configuration values in config.py

- **data_type** (Optional. Default: "text"):

	| data_type       | File type | Encrypted | Valid for                       | Extension |
	|---------------- |-----------|-----------|---------------------------------|-----------|
	| text            | Text file | No        | Google Drive, OneDrive          | .txt      |
	| text_encrypted  | Text file | Yes       | Google Drive, OneDrive          | .txt      |
	| image           | Image     | No        | Google Drive, OneDrive          | .png      |
	| image_encrypted | Image     | Yes       | Google Drive, OneDrive          | .png      |
	| audio           | Audio     | No        | Google Drive, OneDrive          | .wav      |
	| audio_encrypted | Audio     | Yes       | Google Drive, OneDrive          | .wav      |
	| video           | Video     | No        | Google Drive, OneDrive, Youtube | .avi      |
	| video_encrypted | Video     | Yes       | Google Drive, OneDrive, Youtube | .avi      |

- **delay_seconds** (Optional. Default: 300): Seconds between checks of new files uploaded to the Google Drive or OneDrive folder or new videos in the Youtube channel.

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption.

- **debug** (Optional. Default: True): Print messages and timestamps in the listener or not.


--------------------------------------------------------------------------------------

# Google Drive

It allows to execute commands uploading text files, images, audio and videos, unencrypted or encrypted with AES.


```
python3 covert-googledrive.py
```

The listener will check the Google Drive folder every 300 seconds by default (can be updated in *config.py*). In this case a video, "video.avi", is uploaded with the command in the QR of the video.

![img1](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image1.png)

After finding there is a new file uploaded to the folder, it is downloaded, processed and the commands are executed:

![img2](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image2.png)



### Configuration in config.py

- **googledrive_folder**: Url of public Google Drive folder to monitor.


--------------------------------------------------------------------------------------

# Onedrive

It allows to execute commands uploading text files, images, audio and videos, unencrypted or encrypted with AES.


```
python3 covert-onedrive.py
```

The listener will check the OneDrive folder every 300 seconds by default (this can be updated in *config.py*). In this case an audio, "audio_encrypted.wav", is uploaded with the command encrypted with AES.

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image3.png)

After finding there is a new file uploaded to the folder, it is downloaded, processed and the commands are executed:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image4.png)


### Configuration in config.py

- **onedrive_folder**: Url of public OneDrive folder to monitor.


--------------------------------------------------------------------------------------

# Youtube

It allows to execute commands uploading videos, unencrypted or encrypted with AES.

```
python3 covert-youtube.py
```

The listener will check the Youtube channel every 300 seconds by default (this can be updated in *config.py*). First the video is uploaded:

![img5](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image5.png)

After finding there is [a new video in the channel](https://www.youtube.com/watch?v=4hk2g41HyWI), it is downloaded, processed and the commands are executed:

![img6](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image6.png)


### Configuration in config.py

- **youtube_channel_id**: Youtube channel ID of the channel to monitor. You can get it from [here](https://www.youtube.com/account_advanced).

- **youtube_api_key**: Get an API key creating an application and generating the key in [here](https://console.cloud.google.com/apis/credentials).


--------------------------------------------------------------------------------------

# Telegram

Control systems remotely with a Telegram bot. This option does not allow to upload files, but it is possible to send the commands in cleartext ("/cmd") or encrypted with AES ("/encrypted").

```
python3 covert-telegram.py
```

The listener will check the commands in the chat and show the output:

```
/cmd CLEARTEXT_COMMAND
/encrypted AES_ENCRYPTED_COMMAND
```

![img7](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-control/image7.png)


### Configuration in config.py


- **telegram_token**: Bot token, create it using [BotFather](t.me/BotFather). Write "/newbot", then send a name for the bot (for example, "botname") and a username for the bot ending in "-bot" (for example, "somethingrandombot")


--------------------------------------------------------------------------------------

### Installation

```
sudo apt install libzbar0
pip install bs4 Pillow opencv-python pyqrcode pypng pyzbar pycrypto youtube_dl pytesseract python-telegram-bot requests argparse
git clone https://github.com/ricardojoserf/covert-control && cd covert-control/
```

### Creating standalone binaries

```
pyinstaller --onefile covert-googledrive.py
pyinstaller --onefile covert-onedrive.py
pyinstaller --onefile covert-telegram.py
pyinstaller --onefile covert-youtube.py
rm -rf build
rm *spec
ls dist/
```