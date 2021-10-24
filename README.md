# covert-control

- Google Drive - Control systems uploading files to a public Google Drive folder.

- OneDrive - Control systems uploading files to a public OneDrive folder.

- Youtube - Control systems uploading videos to Youtube (migrated from [covert-tube](https://github.com/ricardojoserf/covert-tube)).

- Telegram - Control systems with a Telegram bot.


### Installation

For all the projects:

```
sudo apt install libzbar0
pip install bs4 Pillow opencv-python pyqrcode pypng pyzbar pycrypto youtube_dl pytesseract python-telegram-bot requests argparse
git clone https://github.com/ricardojoserf/covert-control && cd covert-control/
```

--------------------------------------------------------------------------------------

# Google Drive

A program to control systems remotely by uploading files to Google Drive using Python to create the videos and the listener. It allows to upload different types of files, such as text files, images and videos, encrypted or unencrypted. Similar to [covert-tube](https://github.com/ricardojoserf/covert-tube) where I did this using Youtube.

### Create file to upload

It is possible to get the commands to execute from text files (".txt"), images (".png") or videos (".avi").

```
python3 generate_file.py -t TYPE [-o OUTPUTFILE] [-c COMMAND] [-e]
```
- -t (--type) [Required]. Type of file: "video", "image" or "text"

- -o (--outputfile) [Optional]. Output file, with extensions: ".avi" for video, ".png" for image or ".txt" for text files.

- -c (--command) [Optional]. Command to execute.

- -e (--encrypted) [Optional]. Add this flag to encrypt the command with AES.


### Run the listener and upload a file

```
python3 main.py
```

The listener will check the Google Drive folder every 300 seconds by default (can be updated in *config.py*). First a text file is uploaded, then an image and a video:

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image3.jpg)

After finding there is a new file, it is downloaded and the commands are executed:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image4.jpg)

We can see the commands output:

![img5](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image5.jpg)



### Configuration

Update the *config.py* file:

- ***googledrive_folder*** (***Mandatory!!!***) - Url of public Google Drive folder.

- **temp_folder** (Optional. Default: "/tmp/"): Path where images of every frame from the video are stored, with the format *image_*X*.png*.

- **upload_seconds_delay** (Optional. Default: 300): Seconds delay until checking if a new video has been uploaded.

- **data_type** (Optional. Default: "text"): Different types of files to process. 
	- "text" - Generate text file with the command in cleartext
	- "text_encrypted" - Generate text file with the command encrypted with AES
	- "image" - Generate QR image with the command in cleartext
	- "image_encrypted" - Generate QR image with the command encrypted with AES
	- "video" - Generate video file with the command in cleartext
	- "video_encrypted" - Generate video file with the command encrypted with AES

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption, used in the "qr_aes" option.

- **debug** (Optional. Default: True): Print messages or not.


### Installation

For the Google Drive project:

```
sudo apt install libzbar0
pip install bs4 pyzbar pycrypto Pillow opencv-python requests pyqrcode pypng argparse
git clone https://github.com/ricardojoserf/covert-control
cd covert-control/google-drive
```

### Creating a standalone binary

```
pyinstaller --onefile main.py
cp dist/main covert-google-drive
rm -rf dist build
rm main.spec
```

--------------------------------------------------------------------------------------

# Onedrive

A program to control systems remotely by uploading files to OneDrive using Python to create the videos and the listener. It allows to upload different types of files, such as text files, images and videos, encrypted or unencrypted. Similar to [covert-tube](https://github.com/ricardojoserf/covert-tube) where I did this using Youtube.

### Create file to upload

It is possible to get the commands to execute from text files (".txt"), images (".png") or videos (".avi").

```
python3 generate_file.py -t TYPE [-o OUTPUTFILE] [-c COMMAND] [-e]
```
- -t (--type) [Required]. Type of file: "video", "image" or "text"

- -o (--outputfile) [Optional]. Output file, with extensions: ".avi" for video, ".png" for image or ".txt" for text files.

- -c (--command) [Optional]. Command to execute.

- -e (--encrypted) [Optional]. Add this flag to encrypt the command with AES.


### Run the listener and upload a file

```
python3 main.py
```

The listener will check the OneDrive folder every 300 seconds by default (can be updated in *config.py*). First a text file is uploaded, then an image and a video:

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image3.jpg)

After finding there is a new file, it is downloaded and the commands are executed:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image4.jpg)

We can see the commands output:

![img5](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-gdrive/image5.jpg)


### Configuration

Update the *config.py* file:

- **onedrive_folder** (***Mandatory!!!***) - Url of public OneDrive folder.

- **temp_folder** (Optional. Default: "/tmp/"): Path where images of every frame from the video are stored, with the format *image_*X*.png*.

- **upload_seconds_delay** (Optional. Default: 300): Seconds delay until checking if a new video has been uploaded.

- **data_type** (Optional. Default: "text"): Different types of files to process. 
	- "text" - Generate text file with the command in cleartext
	- "text_encrypted" - Generate text file with the command encrypted with AES
	- "image" - Generate QR image with the command in cleartext
	- "image_encrypted" - Generate QR image with the command encrypted with AES
	- "video" - Generate video file with the command in cleartext
	- "video_encrypted" - Generate video file with the command encrypted with AES

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption, used in the "qr_aes" option.

- **debug** (Optional. Default: True): Print messages or not.


### Installation

For the Google Drive project:

```
sudo apt install libzbar0
pip install pyzbar pycrypto Pillow opencv-python requests pyqrcode pypng argparse
git clone https://github.com/ricardojoserf/covert-control
cd covert-control/onedrive
```

### Creating a standalone binary

```
pyinstaller --onefile main.py
cp dist/main covert-onedrive
rm -rf dist build
rm main.spec
```


--------------------------------------------------------------------------------------

# Youtube

A program to control systems remotely by uploading videos to Youtube using Python to create the videos and the listener, emulating some malware I was reading about. It allows to create videos with frames formed of simple text, QR codes with cleartext or QR codes using AES encryption. 

### Create a video

The videos can be created using *generate_video.py*: enter the commands and generate the video writing "exit". The video generated is called by default *output.avi* (can be updated in *config.py*): 

```
python3 generate_file.py -t video -o output.avi -c 'echo "This is a secret" > /tmp/test.txt; whoami > /tmp/whoami.txt; ping -c 3 8.8.8.8 > /tmp/ping.txt'
```

![img1](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image1.png)


### Run the listener and upload the video to Youtube

```
python3 main.py
```

The listener will check the Youtube channel every 300 seconds by default (can be updated in *config.py*). First the video is uploaded:

![img2](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image2.png)

After finding there is [a new video in the channel](https://www.youtube.com/watch?v=ZPQ4drX35bU), it is downloaded and the commands are executed:

![img3](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image3.png)

We can see the output from the commands:

![img4](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-tube/image4.png)



### Configuration

Update the *config.py* file:

- **youtube_channel_id** (Mandatory!!!): Get your Youtube channel ID from [here](https://www.youtube.com/account_advanced).

- **youtube_api_key** (Mandatory!!!): To get the API key create an application and generate the key from [here](https://console.cloud.google.com/apis/credentials).

- **temp_folder** (Optional. Default: "/tmp/"): Path where images of every frame from the video are stored, with the format *image_*X*.png*.

- **delay_seconds** (Optional. Default: 300): Seconds delay until checking if a new video has been uploaded.

- **data_type** (Optional. Default: "text"): Different types of files to process. 
	- "video" - Generate video file with the command in cleartext
	- "video_encrypted" - Generate video file with the command encrypted with AES

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption, used in the "qr_aes" option.

- **debug** (Optional. Default: True): Print messages or not.



### Installation

For Youtube project:

```
sudo apt install libzbar0
pip install Pillow opencv-python youtube_dl pytesseract pyqrcode pypng pyzbar pycrypto
git clone https://github.com/ricardojoserf/covert-control
cd covert-control/youtube
```

### Creating a standalone binary

```
pyinstaller --onefile main.py
cp dist/main covert-tube
rm -rf dist build
rm main.spec
```

--------------------------------------------------------------------------------------

# Telegram

A program to control systems remotely with a Telegram bot.

### Execute command

```
/cmd CLEARTEXT_COMMAND
```

```
/encrypted AES_ENCRYPTED_COMMAND
```

![img1](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image1.png)


### Configuration

Update the *config.py* file:

- ***token*** (***Mandatory!!!***) - Bot token, create it using [t.me/BotFather](t.me/BotFather)

	- Write "/newbot"
	- Send a name for the bot. For example: "botname"
	- Send a username for the bot ending in -bot. For example: "somethingrandombot"

![img2](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image2.png)

- **aes_key** (Optional. Default: "covert-tube_2021"): Key for AES encryption, used in the "qr_aes" option.

### Installation

For the Telegram project:

```
pip install python-telegram-bot pycrypto 
git clone https://github.com/ricardojoserf/covert-control
cd covert-control/telegram
```

### Creating a standalone binary

```
pyinstaller --onefile main.py
cp dist/main covert-telegram
rm -rf dist build
rm main.spec
```

