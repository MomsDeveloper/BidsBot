import asyncio
import configparser
import json

from telethon import TelegramClient, types

CHANNEL_NAME = "Ставки на спорт | STARBET"

config = configparser.ConfigParser()
config.read("config.ini")

API_ID = config['Telethon']['api_id']
API_HASH = config['Telethon']['api_hash']
USERNAME = config['Telethon']['username']

client = TelegramClient(USERNAME, API_ID, API_HASH)
client.start()
client.loop.run_until_complete(client.connect())




async def _get_remote_messages() -> 'dict[int, types.Message]':
	print(0)
	messages_list = [m async for m in client.iter_messages(CHANNEL_NAME, limit=10)]
	messages_dict = {}
	for mmessage in messages_list:
		messages_dict[mmessage.id] = mmessage
	return messages_dict


def get_new_messages() -> 'list[types.Message]':
	
	with client:
		future = asyncio.ensure_future(_get_remote_messages())
		client.loop.run_until_complete(future)
		remote_messages = future.result()

	with open('./data.json', 'r') as f:
		data = json.load(f)
		last_message_id = data['telethon']['last_message_id']
	
	new_messages = []
	for _id in remote_messages:
		if _id != last_message_id:
			new_messages += [remote_messages[_id]]
		else:
			break
	
	if new_messages:
		with open('./data.json', 'w') as f:
			data['telethon']['last_message_id'] = new_messages[0].id
			json.dump(data, f)

	return new_messages


def get_photo_bytes(message: types.Message) -> bytes:
	with client:
		future = asyncio.ensure_future(message.download_media(file=bytes))
		client.loop.run_until_complete(future)
		return future.result()

