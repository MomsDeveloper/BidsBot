import configparser


import schedule
import telebot

from posts_handler import get_new_messages, get_photo_bytes

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config['Telebot']['token']
CHAT_ID = config['Telebot']['chat_id']
TIMEOUT = int(config['Telebot']['timeout'])
bot = telebot.TeleBot(TOKEN)


def send_posts():
	c = 0
	messages = get_new_messages()
	for message in reversed(messages):
		mess_text = message.text
		mess_text = mess_text.replace('**', '')
		if 'Ставим здесь' in mess_text:
			mess_text = mess_text.split('Ставим')[0][:-2]
		elif 'Ставим' in mess_text:
			lines = mess_text.split('\n')
			for i, line in enumerate(lines):
				if 'Ставим' in line:
					mess_text = '\n'.join(lines[:i] + lines[i+2:])
			mess_text = mess_text.split('Ставим')[0]
		if 'Статистика по марафонам' in mess_text:
			mess_text = mess_text.split('Начали')[0][:-2]
		if 'Как забрать бонус' in mess_text or 'Банк' in mess_text or 'Статистика по марафонам' in mess_text or 'Напоминаю' in mess_text or 'ХАЛЯВНЫЕ' in mess_text or 'забираем бонус' in mess_text or 'В банке:' in mess_text:
			c = 1
		else:
			c = 0
			print(c)
		if c != 1:
			if message.photo:
				photo = get_photo_bytes(message)
				bot.send_photo(chat_id=CHAT_ID, photo=photo, caption=mess_text)
			else:			
				bot.send_message(chat_id=CHAT_ID, text=mess_text)


def start_sending():
	bot.send_message(chat_id=CHAT_ID, text='start')
	schedule.every(TIMEOUT).seconds.do(send_posts)
	while 1:
		schedule.run_pending()


if __name__ == '__main__':
	start_sending()
