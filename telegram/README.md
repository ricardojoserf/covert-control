# Telegram

A program to control systems remotely with a Telegram bot.

### Execute command

```
/cmd COMMAND
```

![img1](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image1.png)


### Configuration

Update the *config.py* file:

- ***token*** (***Mandatory!!!***) - Bot token, create it using [t.me/BotFather](t.me/BotFather)

	- /newbot
	- botname
	- somethingrandombot

![img2](https://raw.githubusercontent.com/ricardojoserf/ricardojoserf.github.io/master/images/covert-telegram/image2.png)

### Installation

For the Telegram project:

```
pip install python-telegram-bot
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

