# -*- coding: utf-8 -*-
import telebot
import config
import workerrs
import re
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from random import randint

bot = telebot.TeleBot(config.token)

month = None
team = None
pict = ['https://whccska.ru/media/photo/fotoreportazh-s-matcha-kuban-cska/#jp-carousel-6941',
        'https://whccska.ru/media/photo/fotoreportazh-s-matcha-zvezda-cska/#jp-carousel-7456',
        'https://whccska.ru/media/photo/fotoreportazh-s-matcha-cska-agu-adyif/#jp-carousel-7053',
        'https://whccska.ru/media/photo/fotoreportazh-pervaja-trenirovka-armejcev-posle-otpuska/#jp-carousel-7839',
        'https://whccska.ru/media/photo/fotoreportazh-s-matcha-cska-kuban/#jp-carousel-7165'

        ]
pict_hockey = ['https://cska-hockey.ru/photos/gallery/2020_02_27_tsska_khk_sochi/'
               'https://cska-hockey.ru/photos/gallery/2020_03_02_pley_off_kubka_gagarina_pervaya_igra_tsska_torpedo/?PAGEN_1=2',
               'https://cska-hockey.ru/photos/gallery/2020_03_02_pley_off_kubka_gagarina_pervaya_igra_tsska_torpedo/?PAGEN_1=4']

def schedule_basket():
    url = 'https://cskabasket.com/schedule/'
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    field_list = []
    for i in range(0, 4):
        col = list()
        col.append(rows[0].find_all('td')[i + 1].get_text().strip('*'))  # заголовок
        for row in rows[1::2]:  #через одну, т.к. инфа об одном матче в 2-х строках
            r = row.find_all('td')
            col.append(r[i + 1].get_text().strip())
        field_list.append(col)
    d = dict()
    for i in range(0, 4):
        d[field_list[i][0]] = field_list[i][1:]
    df = pd.DataFrame(d)
    #TODO ограничить выборку
    # TODO убрать первый столбец
    df.head()
    return df


def schedule_rugby():
    url = 'https://cskabasket.com/schedule/'
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')

    url = 'https://www.cska-rugby.ru/calendar/vstrechi-rezultaty/'
    website = requests.get(url).text
    soup = BeautifulSoup(website, 'lxml')
    table = soup.find_all('table')[2]
    rows = table.find_all('td')

    field_list = []
    for i in range(0, len(rows)):
        #         col = []
        #         col.append('Лига')
        #         for row in rows[0:]:
        #             col.append(row.find_all('h3')[0].text)
        #     field_list.append(col)
        col1 = []
        col1.append('Время')
        for row in rows[0:]:
            col1.append(row.find_all('time', {'itemprop': 'startDate'})[0].attrs['datetime'].strip())
    field_list.append(col1)
    col2 = []
    col2.append('Команда 1')
    for row in rows[0:]:
        col2.append(row.find_all('meta', {'itemprop': 'name'})[0].attrs['content'])
    field_list.append(col2)
    col3 = []
    col3.append('Команда 2')
    for row in rows[0:]:
        col3.append(row.find_all('meta', {'itemprop': 'name'})[1].attrs['content'])
    field_list.append(col3)

    d = dict()
    for i in range(0, 3):
        d[field_list[i][0]] = field_list[i][1:]
    df = pd.DataFrame(d)
    df['Дата'] = [t.split(' ')[0] for t in df.Время]
    df['Время'] = [t.split(' ')[1] for t in df.Время]
    df.head()
    return df



# Начало диалога
@bot.message_handler(content_types=["start"])
def cmd_start(message):
    workerrs.set_state(message.chat.id, config.States.S_START.value)
    state = workerrs.get_current_state(message.chat.id)
    bot.send_message(message.chat.id, "Приветствую болельщиков ЦСКА!!! \n"
                                      "Этот бот позволяет узнать расписание любимого клуба.\n"
                                      "Выберите команду (/team) расписание которой вас интересует.\n"
                                      "Выберите /reset чтобы вернуться назад и начать заново")
    bot.send_photo(message.chat.id, pict[randint(0, 3)])
    workerrs.set_state(message.chat.id, config.S_ENTER_TEAM.value)

# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Начнем сначала.\n"
                                      "Что выбираешь: /month (в разработке) or /team.")
    workerrs.set_state(message.chat.id, config.States.S_ENTER_TEAM.value)

@bot.message_handler(commands=["month"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Введите номер месяца для поиска:\n")
    num=int(input())

@bot.message_handler(commands=["team"])
def cmd_commands(message):
    bot.send_message(message.chat.id, "/football (в разработке)\n"
                                      "/basketball \n"
                                      "/hockey (в разработке)\n"
                                      "/rugby \n"
                                      "/handball (в разработке)")

@bot.message_handler(commands=["football"])
def enter_field_list(message):
    bot.send_message(message.chat.id, 'Раздел пока не готов, автор запарился парсить')
    #bot.send_photo(message.chat.id, pict[randint(0, 3)])
    #bot.send_message(message.chat.id, tabulate(x, headers=x.columns, tablefmt="pipe"))

@bot.message_handler(commands=["hockey"])
def enter_field_list(message):
    bot.send_message(message.chat.id, 'Лето на дворе, какой хоккей?! GO на футбол')
    bot.send_photo(message.chat.id, pict_hockey[randint(0, 2)])

@bot.message_handler(commands=["rugby"])
def enter_field_list(message):
    bot.send_message(message.chat.id, 'Суровая игра, думать буду, но недолго')

    y = schedule_rugby()
    bot.send_message(message.chat.id, tabulate(y, headers=y.columns, tablefmt="pipe"))
@bot.message_handler(commands=["handball"])
def enter_field_list(message):
    bot.send_message(message.chat.id, 'Ты уверен, что хочешь это посмотреть? \n'
                                       'Я не особо, поэтому и расписания не будет \n'
                                       'Хотя ...')
    bot.send_photo(message.chat.id, pict[randint(0, 4)])



@bot.message_handler(commands=["basketball"])
def enter_field_list(message):
    bot.send_message(message.chat.id, 'Ok, проверяю информацию.')
    x = schedule_basket()
    bot.send_message(message.chat.id, tabulate(x, headers=x.columns, tablefmt="pipe"))


@bot.message_handler(func=lambda message: message.text not in ('/reset', '/team', '/start', '/month'))
def cmd_sample_message(message):
    bot.send_message(message.chat.id, "Приветствую болельщиков ЦСКА!!! \n"
                                      "Этот бот позволяет узнать расписание любимого клуба.\n"
                                      "Выберите месяц (/month) (в разработке) на который вы хотите посмотреть расписание.\n"
                                      "Выберите команду (/team) расписание которой вас интересует.\n"
                                      "Выберите /reset чтобы вернуться назад и начать заново")

if __name__ == "__main__":
    bot.infinity_polling()

