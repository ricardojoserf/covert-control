from telegram.ext import Updater, CommandHandler
from telegram.ext.dispatcher import run_async
import subprocess
import config


def exec_cmd(command):
	try:
		sub_ = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		subprocess_return = sub_.stdout.read()
		return subprocess_return.decode("utf-8") 
	except:
		return "There was an error executing the command"


def cmd(update, context):
	chat_id = update.message.chat_id
	command = " ".join(context.args)
	subprocess_return = exec_cmd(command)
	context.bot.sendMessage(chat_id, subprocess_return)


def main():
	token = config.telegram_token
	updater = Updater(token, use_context=True)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('cmd',cmd))
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
    main()
