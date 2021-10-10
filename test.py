from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sync import TelegramClient
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telethon']['api_id']
api_hash = config['Telethon']['api_hash']
username = config['Telethon']['username']


client = TelegramClient(username, api_id, api_hash)
client.start()
client.connect()
for i in client.get_dialogs():
    print(i.name, i.id)