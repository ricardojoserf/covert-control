# covert-control

- Google Drive - Control systems uploading files to a public folder in Google Drive.

- OneDrive - Control systems uploading files to a public folder in OneDrive.

- Telegram - Control systems with a Telegram bot.

- Youtube - Control systems uploading videos to Youtube (updated from [covert-tube](https://github.com/ricardojoserf/covert-tube)).


### Installation

```
sudo apt install libzbar0
pip install bs4 Pillow opencv-python pyqrcode pypng pyzbar pycrypto youtube_dl pytesseract python-telegram-bot requests argparse
git clone https://github.com/ricardojoserf/covert-control && cd covert-control/
```

### Create files to upload

It is possible to execute commands from text files (".txt"), images (".png"), audio (".wav") or videos (".avi") in the case of Google Drive and OneDrive, and only videos in the case of Youtube. You can also find example files in the folder test_files.

```
python3 generate_file.py -t TYPE [-o OUTPUTFILE] [-c COMMAND] [-e]
```
- -t (--type) [Required]. Types of file: "text", "image", "audio" or "video": 

- -o (--outputfile) [Optional]. Output file, with extension ".txt" for "text", ".png" for "image", ".wav" for "audio" and ".avi" for "video"

- -c (--command) [Optional]. Command to execute.

- -e (--encrypted) [Optional]. Add this flag to encrypt the command with AES.


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

- **delay_seconds** (Optional. Default: 300): Seconds delay until checking if a new video has been uploaded.

- **data_type** (Optional. Default: "text"):
	- "text" - Generate text file with the command in cleartext
	- "text_encrypted" - Generate text file with the command encrypted with AES
	- "image" - Generate QR image with the command in cleartext
	- "image_encrypted" - Generate QR image with the command encrypted with AES
	- "video" - Generate video file with the command in cleartext
	- "video_encrypted" - Generate video file with the command encrypted with AES

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption, used in the "qr_aes" option.

- **debug** (Optional. Default: True): Print messages or not.


--------------------------------------------------------------------------------------

# Google Drive

It allows to execute commands uploading text files, images, audio and videos, unencrypted or encrypted with AES.


```
python3 covert-googledrive.py
```

The listener will check the Google Drive folder every 300 seconds by default (can be updated in *config.py*). First a text file is uploaded, then an image and a video:

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image3.jpg)

After finding there is a new file in the folder, it is downloaded, processed and the commands are executed:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image4.jpg)


### Configuration in config.py

- ***googledrive_folder*** (***Mandatory!!!***) - Url of public Google Drive folder.



--------------------------------------------------------------------------------------

# Onedrive

It allows to execute commands uploading text files, images, audio and videos, unencrypted or encrypted with AES.


```
python3 covert-onedrive.py
```

The listener will check the OneDrive folder every 300 seconds by default (can be updated in *config.py*).

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image3.jpg)

After finding there is a new file in the folder, it is downloaded, processed and the commands are executed:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image4.jpg)


### Configuration in config.py

- **onedrive_folder** (***Mandatory!!!***) - Url of public OneDrive folder.


--------------------------------------------------------------------------------------

# Youtube

It allows to execute commands uploading videos, unencrypted or encrypted with AES.

```
python3 covert-youtube.py
```

The listener will check the Youtube channel every 300 seconds by default (can be updated in *config.py*). First the video is uploaded:

![youtube-video-uploaded](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image2.png)

After finding there is [a new video in the channel](https://www.youtube.com/watch?v=ZPQ4drX35bU), it is downloaded, processed and the commands are executed:

![youtube-commands](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image3.png)


### Configuration in config.py

- **youtube_channel_id** (Mandatory!!!): Get your Youtube channel ID from [here](https://www.youtube.com/account_advanced).

- **youtube_api_key** (Mandatory!!!): To get the API key create an application and generate the key from [here](https://console.cloud.google.com/apis/credentials).


--------------------------------------------------------------------------------------

# Telegram

Control systems remotely with a Telegram bot.

```
python3 covert-telegram.py
```

In the bot chat:

```
/cmd CLEARTEXT_COMMAND
/encrypted AES_ENCRYPTED_COMMAND
```

![telegram-bot](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image1.png)


### Configuration

Update the *config.py* file:

- ***telegram_token*** (***Mandatory!!!***) - Bot token, create it using [t.me/BotFather](t.me/BotFather). Write "/newbot", then send a name for the bot (for example, "botname") and finally send a username for the bot ending in -bot (for example, "somethingrandombot")

![img2](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image2.png)



--------------------------------------------------------------------------------------

### Creating standalone binaries

```
pyinstaller --onefile covert-googledrive.py
cp dist/main covert-googledrive
pyinstaller --onefile covert-onedrive.py
cp dist/main covert-onedrive
pyinstaller --onefile covert-telegram.py
cp dist/main covert-telegram
pyinstaller --onefile covert-youtube.py
cp dist/main covert-youtube
rm -rf dist build
rm main.spec
```

