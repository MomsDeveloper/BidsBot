import telebot
import json
import datetime
import time
from selenium import webdriver


bot = telebot.TeleBot('1801366537:AAHbo9piW7vZc_MrBqqB7ws-q3QX4H2cjcw')
joinedFile = open('idies.txt', 'r')
joinedUsers = set()
for line in joinedFile:
    joinedUsers.add(line.strip())
joinedFile.close()

class ProgHubParser(object):
    def __init__(self):
        driver = webdriver.Chrome(r'D:\Users\eduar\Desktop\Work\chromedriver.exe')
        self.driver = driver


    def bids_parser(self):
        self.driver.get('https://vprognoze.ru/forecast/newbie/fcufootball/')
        bid_cards = self.driver.find_elements_by_class_name('tip-line__info')
        
        self.gamename_list = []


        k = 0
        c = 0
        self.game_info = []
        self.gamename = []
        self.forecast_list = [] #прогноз
        self.ratio_list = []#коэффициент
        summa_list = []
        self.game_ivent = [] 
        
        game_ivent = self.driver.find_elements_by_class_name('tip-card__league')
        for i in game_ivent:
            self.game_ivent.append(i.text)

        game_info = self.driver.find_elements_by_class_name('ui-expand__content')
        for i in game_info:
            self.game_info.append(i.text)

        ds = self.driver.find_elements_by_class_name('tip-card__teams')
        for i in ds:
            self.gamename.append(i.text.replace('\n', ' '))
        for card in bid_cards:
            k+=1
            if k == 1:
                self.forecast_list.append(card.text)

            elif k == 2:
               self.ratio_list.append(card.text)
            elif k == 3:
                summa_list.append(card.text)

                k = 0

        if self.forecast_list[c] == 'Ничья':
            c+=1
        bot.send_message(channel, f'{self.game_ivent[c]} \n \n{self.gamename[c]} \n \nПрогноз: {self.forecast_list[c]}   Кф: {self.ratio_list[c]} \n ---------------   ')
        self.driver.quit()
        

with open('config.json') as file:
    config = json.load(file
    )
    
while True:
    k = 0
    now = datetime.datetime.now()
    
    

    if str(now.strftime("%H:%M:%S"))=='12:00:00':
        
        for channel in config['CHANNEL_LOGIN']:

            bot.send_message(channel, f"🚀Сегодня начинаем ставить🚀 \n ✅Включайте уведомления и ожидайте \n \nЕсли есть какие то вопросы по VIP чату и подробному разбору каждого матча писать сюда-(ссылка на вип чат)\n \n🌐Если вы не знаете где ставить и как, то мы проконсультируем вас \n 🔔Писать сюда:(ссылка) \n \n🍀Всем удачи и поехали‼️")
            time.sleep(10)
    elif str(now.strftime("%H:%M:%S"))=='12:10:00':
        for channel in config['CHANNEL_LOGIN']:

            bot.send_message(channel, f'〽️Всем доброго времени суток〽️ \n \n     🤑Скоро начинаем ставить🤑 \n \n Кто не знает как, мы бесплатно обучаем! ')
            markup = telebot.types.InlineKeyboardMarkup()
            btn_my_site= telebot.types.InlineKeyboardButton(text='Наш эксперт', url='https://t.me/vfa_rus')
            bot.send_message(channel, "По вопросам⬇️", reply_markup = markup)
            markup.add(btn_my_site)

            parser = ProgHubParser()
            parser.bids_parser()

    # if abs(12-int(now.strftime("%H")))%3 == 0 and str(now.strftime("%M:%S")).count('0')==4:
    for channel in config['CHANNEL_LOGIN']:
        parser = ProgHubParser()
        parser.bids_parser()            
