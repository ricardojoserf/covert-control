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

--------------------------------------------------------------------------------------

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
