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

