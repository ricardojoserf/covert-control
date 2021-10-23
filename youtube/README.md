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

--------------------------------------------------------------------------------------

### Youtube Configuration

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

## Motivation

Lately I have been reading about malware using Youtube for controlling their setting remotely. For example, Casbaneiro abuses YouTube to store its C&C server domains. Each video on the channels used by the threat actor contains a description and at the end of these there is a link to a bogus Facebook or Instagram url containing the C&C server domain ([Welivesecurity blog](https://www.welivesecurity.com/2019/10/03/casbaneiro-trojan-dangerous-cooking/)). A second example is Numando, which abuses it by encrypting the data in the title of the Youtube videos ([other Welivesecurity blog](https://www.welivesecurity.com/2021/09/17/numando-latam-banking-trojan/)). 

Knowing this I decided to create a PoC to test the control of remote systems uploading videos to Youtube but, instead of using the title or the description, using the content of the video. It allows to execute any command, but it could be used to change some settings remotely. So this is just a PoC, use it for educational purposes!
