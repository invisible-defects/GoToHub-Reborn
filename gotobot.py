#! ~/.local/bin/env python3
# coding: utf8

import time as tm
import telebot
from telebot import types
import json
from threading import Timer
# чтение json файла с данными о участниках
def readmembers():
    data = json.load(open('members.json', 'r', encoding="utf-8"))
    return data

# запись в json файл данных о участниках
def writemembers(text):
    with open("members.json", "w", encoding="utf-8") as file:
        json.dump(text, file)

# чтение json файла с информацией о смене
def readinfo():
    data = json.load(open('info.json', 'r'))
    return data

# запись в json файл информацию о смене
def writeinfo(text):
    with open("info.json", "w", encoding="utf-8") as file:
        json.dump(text, file)

# чтение json файла с информацией о квесте
def readquest():
    data = json.load(open('quest.json', 'r'))
    return data

# запись в json файл информацию о квесте
def writequest(text):
    with open("quest.json", "w", encoding="utf-8") as file:
        json.dump(text, file)

def writeachives(text):
    with open("achives.json", "w", encoding="utf-8") as file:
        json.dump(text, file)

def readachives():
    data = json.load(open('achives.json', 'r'))
    return data


#узнаем токен нашего бота
bot = telebot.TeleBot(readinfo()['token'])

# Функция ФСБ: узнаем инфу о пользователе
def checker(message):
    members = readmembers()['members']
    idmember = ''
    nameofuser = ''
    typeofuser = 0
    for i in range(len(members)):
        if str(message.chat.id) == str(members[i]['id']):
            # idmember=int(members[i]['id'])
            idmember = i
            typeofuser = int(members[i]['admin'])
            if members[i]['name'] != '':
                nameofuser = members[i]['name']
    if idmember == '':
        return ([0, 0, 0])
    else:
        return ([typeofuser, idmember, nameofuser])

#Украшаем вывод расписания
def schedulizer(schedule):
    schedule = schedule.split("\n")
    for j in range(len(schedule)):
        schedule[j] = "<b>" + str(schedule[j][:5]) + "</b>" + str(schedule[j][5:])
    schedule = "\n".join(schedule)
    return schedule

# Юзерская клавиатура
usermarkup = types.ReplyKeyboardMarkup(True, False)
usermarkup.row('🗓 Расписание', '⛳️ Событие')
usermarkup.row('🏅 Ачивки', '❗️ Информация')
usermarkup.row('🛠 Комманды')
# Админская клавиатура
adminmarkup = types.ReplyKeyboardMarkup(True, False)
adminmarkup.row('🗓 Расписание', '⛳️ Событие')
adminmarkup.row('🏅 Ачивки', '❗️ Информация')
adminmarkup.row('🛠 Комманды', '🔒 Админка')
# Админка
adminkamarkup = types.ReplyKeyboardMarkup(True, False)
adminkamarkup.row('📆 Расписание', '🎖 Ачивки')
adminkamarkup.row('🏠 Где я живу?', '📞 Контакты')
adminkamarkup.row('✉️ Срочное сообщение')
adminkamarkup.row('❌ Выход')
#Убрать клаву
hidemarkup = types.ReplyKeyboardRemove()


def eventmessanger():
    members = readmembers()['members']
    data = readinfo()['schedule']
    quest = readquest()
    if int(quest['quest']) == 1:
        if int(quest['activate']) == 0:
            usermarkup = types.ReplyKeyboardMarkup(True, False)
            usermarkup.row('🗓 Расписание', '⛳️ Событие')
            usermarkup.row('🏅 Ачивки', '❗️ Информация')
            usermarkup.row('🛠 Комманды','🎮 Квест')
            for j in range(len(members)):
                if int(members[j]['admin'])!=2:
                    bot.send_message(int(members[j]['id']),
                    "<b>Начало квеста!</b>\n\nВыберите кнопку 🎮 Квест или введите команду /quest. Далее следуйте инструкции! "
                    ,parse_mode="HTML",reply_markup=usermarkup)
            quest['activate']="1"
            writequest(quest)
    if data!='':
        schedule = schedulizer(data)
        localtime = int(tm.localtime()[3] * 60 + tm.localtime()[4])
        if localtime==8*60:
            for j in range(len(members)):
                bot.send_message(int(members[j]['id']), schedule,parse_mode="HTML")
        data = data.split("\n")
        times = data
        for i in range(len(times)):
            times[i] = times[i][:5]
            times[i] = int(times[i].split(":")[0]) * 60 + int(times[i].split(":")[1])
        for i in range(len(times)):
            if localtime == times[i]-10:
                data = readinfo()['schedule']
                data = data.split("\n")
                text=data[i]
                for j in range(len(members)):
                    bot.send_message(int(members[j]['id']), "<b>"+text[:5]+"</b>"+text[5:],parse_mode="HTML")
                break
        interval=Timer(59.0, eventmessanger)
        interval.start()
eventmessanger()

@bot.message_handler(commands=["start"])
def start(message):
    auth = checker(message)
    # Проверка на "существовние" пользователя
    if auth[0] == 0:
        start = bot.send_message(message.chat.id, "Чтобы продолжить работу введи код!")
        bot.register_next_step_handler(start, register)
    # Если обычный юзер
    elif auth[0] == 1:
        bot.send_message(message.chat.id, "Приветствую тебя, " + str(auth[2]) + ".", reply_markup=usermarkup)
        bot.send_sticker(message.chat.id, "CAADBAADXQcAAhXc8gKXC24wqNJ1GgI")
    # Если админ
    elif auth[0] == 2:
        bot.send_message(message.chat.id, "Приветствую тебя, " + str(auth[2]) + ".", reply_markup=adminmarkup)
        bot.send_sticker(message.chat.id, "CAADBAADXQcAAhXc8gKXC24wqNJ1GgI")

# Если новый юзер - добавление в систему и его регистраця
def register(message):
    auth = checker(message)
    data = readmembers()
    authorized=0
    for i in range(len(data['members'])):
        if str(message.chat.id)==str(data['members'][i]['id']):
            authorized=1
            if str(message.text) == str(readinfo()['admincode']):
                bot.send_message(message.chat.id, "И снова здравствуйте, "+str(auth[2])+"!",reply_markup=adminmarkup)
                bot.send_sticker(message.chat.id,"CAADBAADWwcAAhXc8gIsyPgYvm7gcAI")
                data['members'][i]['admin']=2
                writemembers(data)
            if str(message.text) == str(readinfo()['usercode']):
                bot.send_message(message.chat.id, "И снова здравствуйте, " + str(auth[2])+"!", reply_markup=usermarkup)
                bot.send_sticker(message.chat.id, "CAADBAADWwcAAhXc8gIsyPgYvm7gcAI")
                data['members'][i]['admin'] = 1
                writemembers(data)
            if str(message.text) != str(readinfo()['usercode']) and str(message.text) != str(readinfo()['admincode']):
                wrong = bot.send_message(message.chat.id, "Введен не верный код")
                bot.register_next_step_handler(wrong, register)

    if authorized==0:
        if str(message.text) == str(readinfo()['admincode']):
            data['members'].append({"id": str(message.chat.id), "admin": "2", "name": "", "achives": []})
            writemembers(data)
            reg = bot.send_message(message.chat.id, "Введи свое Имя и Фамилию в формате: «Василий Пупкин».")
            bot.register_next_step_handler(reg, database)
        if str(message.text) == str(readinfo()['usercode']):
            data['members'].append({"id": str(message.chat.id), "admin": "1", "name": "", "achives": []})
            writemembers(data)
            reg = bot.send_message(message.chat.id, "Введи свое Имя и Фамилию в формате: «Василий Пупкин».")
            bot.register_next_step_handler(reg, database)
        if str(message.text) != str(readinfo()['usercode']) and str(message.text) != str(readinfo()['admincode']):
            wrong = bot.send_message(message.chat.id, "Введен не верный код")
            bot.register_next_step_handler(wrong, register)

def database(message):
    data = readmembers()
    auth = checker(message)
    data['members'][auth[1]]['name'] = message.text
    writemembers(data)
    if auth[0] == 1:
        bot.send_message(message.chat.id, "Хэй, привет друг!", reply_markup=usermarkup)
    elif auth[0] == 2:
        bot.send_message(message.chat.id, "Здравствуйте, ваше превосходительство!", reply_markup=adminmarkup)


# Пользователь свалил :(
@bot.message_handler(commands=["stop"])
def handle_stop(message):
    data = readmembers()
    auth = checker(message)
    data['members'][auth[1]]['admin']=0
    writemembers(data)
    bot.send_message(message.chat.id, "Ты уже уходишь...", reply_markup=hidemarkup)
    bot.send_sticker(message.chat.id, "CAADAgADdwoAAkKvaQABg_wS9u8cP_kC")


# Пользователю нужна помощь!
@bot.message_handler(func=lambda message: message.text == "🛠 Комманды" or message.text == "/help")
def handle_help(message):
    auth = checker(message)
    if auth[0] == 0:
        start(message)
    elif auth[0] == 1:
        bot.send_message(message.chat.id,
                         "🗓 Расписание, /schedule - полное расписание на день.\n⛳️ Событие, /event - «Что и где сейчас?».\n❗️ Информация, /info - «Где я живу?», номера телефонов.\n🛠 Комманды, /help - описание комманд бота.")
    elif auth[0] == 2:
        bot.send_message(message.chat.id,
                         "🔒 Админка, /admin - административная система\n"
                         "🗓 Расписание, /schedule - полное расписание на день.\n"
                         "Для изменения расписания 📆 Расписание, /editschedule \n"
                         "⛳️ Событие, /event - «Что и где сейчас?»\n"
                         "❗️ Информация, /info - «Где я живу?», номера телефонов\n"
                         "Для изменения информации о проживании 🏠 Где я живу?, /editadress.\n"
                         "Для изменения контактной информации 📞 Контакты, /editphones\n"
                         "🛠 Комманды, /help - описание комманд бота\n"
                         "✉️ Срочное сообщение, /quickmessage - рассылка срочных сообщений\n"
                         "❌ Выход, /exit - выход из административного режима.")



# Запрашиваем расписание
@bot.message_handler(func=lambda message: message.text == "🗓 Расписание" or message.text == "/schedule")
def handle_schedule(message):
    auth = checker(message)
    if auth[0] != 0:
        # Читаем расписание
        schedule = str(readinfo()['schedule'])
        if schedule!='':
            schedule = schedulizer(schedule)
            bot.send_message(message.chat.id, str(schedule), parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "<b>Ещё не добавили расписание.</b>", parse_mode="HTML")
            bot.send_sticker(message.chat.id,"CAADAgADswoAAkKvaQABaMOVR9paPiQC")
    else:
        start(message)


# Рассказываем о каких-то происходящих в данное время событиях
@bot.message_handler(func=lambda message: message.text == "⛳️ Событие" or message.text == "/event")
def handle_event(message):
    auth = checker(message)
    if auth[0] != 0:
        data = readinfo()['schedule']
        if data!='':
            data = data.split("\n")
            times = data
            # какой-то сложный код с костылями (лучше не смотреть)
            for j in range(len(times)):
                times[j] = times[j][:5]
                times[j] = int(times[j].split(":")[0]) * 60 + int(times[j].split(":")[1])
            localtime = int(tm.localtime()[3] * 60 + tm.localtime()[4])
            data = readinfo()['schedule']
            data = data.split("\n")
            for j in range(len(times) - 1):
                if localtime < times[j]:
                    text = data[j - 1]
                    text = "<b>" + text[:5] + "</b>" + text[5:]
                    bot.send_message(message.chat.id, str(text), parse_mode="HTML")
                    break
                if localtime < times[0]:
                    if times[0] - localtime < 120:
                        bot.send_message(message.chat.id, "Следующее мероприятие" + str(data[0]))
                    else:
                        bot.send_message(message.chat.id, "Больше не запланировно никаких мероприятий")
                if j == (len(times) - 2):
                    if (localtime - times[-1]) < 120:
                        bot.send_message(message.chat.id, str(data[-1]))
                    else:
                        bot.send_message(message.chat.id, "Больше не запланировно никаких мероприятий")
        else:
            bot.send_message(message.chat.id, "<b>Ещё не добавили расписание.</b>", parse_mode="HTML")
            bot.send_sticker(message.chat.id, "CAADAgADswoAAkKvaQABaMOVR9paPiQC")
    else:
        start(message)


# Рассказываем пользователю, чего он добился в своей жизни (Обычно бот отвечает: "Список достижений пуст.")
@bot.message_handler(func=lambda message: message.text == "🏅 Ачивки" or message.text == "/achives")
def achives(message):
    data = readmembers()
    auth = checker(message)
    if auth[0] != 0:
        achives = data['members'][auth[1]]['achives']
        if len(achives) != 0:
            new = []
            for i in range(len(achives)):
                new.append(achives[i]['name'] + "\n")
            new.reverse()
            stroke = '<b>Твои ачивки</b>\n\n'
            for i in range(1, len(new) + 1):
                stroke += str(i) + ". " + str(new[i - 1])
            bot.send_message(message.chat.id, stroke,parse_mode="HTML")
        else:
            bot.send_message(message.chat.id, "<b>У тебя пока нет ачивок.</b>", parse_mode="HTML")
            bot.send_sticker(message.chat.id, "CAADBAADcAcAAhXc8gJyeBay5IC2QAI")
    else:
        start(message)
def deletelog(message):
    data = readmembers()['members']
    stroke = ''
    kol=len(data)
    number=int(message.text)
    if number>=1 and number<=len(data):
        for i in range(1, kol):
            if i==number:
                stroke = 'Введите номер ачивки, которую надо удалить.\n<b>Пользователь: </b>'+data[i - 1]['name']+"\n\n"
                for j in range(len(data[i - 1]['achives'])):
                    stroke += str(j+1) + ". " + str(data[i - 1]['achives'][j]['name']) + "\n"
                send=bot.send_message(message.chat.id,stroke,parse_mode="HTML")
                achives=readachives()
                achives['deleteachive'].append({"iduser":int(data[i - 1]['id'])})
                writeachives(achives)
                bot.register_next_step_handler(send,decision)
                    
    else:
        send=bot.send_message(message.chat.id,"Неправильно введен номер пользователя или пользователя с таким номером не существует! Введите заново.")
        bot.register_next_step_handler(send,deletelog)

def decision(message):
    achives=readachives()['deleteachive']
    members=readmembers()['members']
    #try:
    for i in range(len(members)):
        for j in range(len(achives)):
            if int(members[i]['id'])==achives[j]['iduser']:
                bot.send_message(message.chat.id,
                                 "<b>Удалена ачивка!\n"
                                 "Пользователь:</b>"+members[i]['name']+
                                 "\n<b>Название ачивки:</b>"+members[i]['achives'][int(message.text)-1]['name'],parse_mode="HTML")
                del members[i]['achives'][int(message.text)-1]
                del achives[j]
                writeachives({'deleteachive': achives})
                writemembers({'members':members})
                break
    #except IndexError:
    #    send=bot.send_message(message.chat.id, "Нет ачивки с таким номером введи заново!")
    #    bot.register_next_step_handler(send,decision)

def addition(message):
    print('sd')
#Рассказываем ему нужную (нет) информацию
@bot.message_handler(func=lambda message: message.text == "❗️ Информация" or message.text == "/info")
def handle_info(message):
    auth = checker(message)
    if auth[0]!=0:
        markup = types.InlineKeyboardMarkup()
        whereilive = types.InlineKeyboardButton(text='🏡 Где я живу?', callback_data='whereilive')
        phones = types.InlineKeyboardButton(text='☎️ Контакты', callback_data='phones')
        markup.add(whereilive, phones)
        bot.send_message(message.chat.id, "Выбери вариант:", reply_markup=markup)
    else:
        start(message)


@bot.message_handler(func=lambda message: message.text == "🔒 Админка" or message.text == "/admin")
def handle_admin(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            bot.send_message(message.chat.id, "<b>Включён административный режим</b>", parse_mode="HTML",
                             reply_markup=adminkamarkup)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


@bot.message_handler(func=lambda message: message.text == "📆 Расписание" or message.text == "/editschedule")
def editschedule(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            cancel = types.InlineKeyboardMarkup()
            can = types.InlineKeyboardButton(text='❌ Отмена', callback_data='continue')
            sub = types.InlineKeyboardButton(text='✅ Продолжить', callback_data='newschedule')
            cancel.add(can, sub)
            bot.send_message(message.chat.id,
                             "<b>Введите расписание в формате:</b>\n08:00 Первое событие\n20:00 Второе событие",
                             parse_mode="HTML", reply_markup=cancel)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


def newschedule(message):
    data = readinfo()
    data['schedule'] = str(message.text)
    writeinfo(data)
    schedule = str(message.text)
    schedule = schedule.split("\n")
    for j in range(len(schedule)):
        schedule[j] = "<b>" + str(schedule[j][:5]) + "</b>" + str(schedule[j][5:])
    schedule = "\n".join(schedule)
    data = readmembers()
    for j in range(len(data['members'])):
        if str(data['members'][j]['id']) != str(message.chat.id):
            bot.send_message(int(data['members'][j]['id']), "<b>Расписание обновлено!</b>\n\n"+str(schedule), parse_mode="HTML")
    bot.send_message(message.chat.id, "<b>Расписание обновлено!</b>\n", parse_mode="HTML",reply_markup=adminkamarkup)


@bot.message_handler(func=lambda message: message.text == "🏠 Где я живу?" or message.text == "/editadress")
def editadress(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            cancel = types.InlineKeyboardMarkup()
            can = types.InlineKeyboardButton(text='❌ Отмена', callback_data='continue')
            sub = types.InlineKeyboardButton(text='✅ Продолжить', callback_data='newadress')
            cancel.add(can, sub)
            bot.send_message(message.chat.id, "<b>Введите новую информацию о проживании.</b>", parse_mode="HTML",
                             reply_markup=cancel)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


def newadress(message):
    data = readinfo()
    data['adress'] = str(message.text)
    writeinfo(data)
    data=readmembers()
    for i in range(len(data['members'])):
        if str(data['members'][i]['id']) != str(message.chat.id):
            bot.send_message(int(data['members'][i]['id']), "<b>Новое расписание!</b>\n" + str(message.text),parse_mode="HTML")
    bot.send_message(message.chat.id, "<b>Информация о проживании обновлена!</b>", parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "📞 Контакты" or message.text == "/editphones")
def editphones(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            cancel = types.InlineKeyboardMarkup()
            can = types.InlineKeyboardButton(text='❌ Отмена', callback_data='continue')
            sub = types.InlineKeyboardButton(text='✅ Продолжить', callback_data='newphones')
            cancel.add(can, sub)
            bot.send_message(message.chat.id, "<b>Введите новую контактную информацию.</b>", parse_mode="HTML",
                             reply_markup=cancel)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


def newphones(message):
    data = readinfo()
    data['info'] = str(message.text)
    writeinfo(data)
    bot.send_message(message.chat.id, "<b>Контактная информация обновлена!</b>", parse_mode="HTML",
                     reply_markup=adminkamarkup)


@bot.message_handler(func=lambda message: message.text == "✉️ Срочное сообщение" or message.text == "/quickmessage")
def handle_quickmessage(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            cancel = types.InlineKeyboardMarkup()
            can = types.InlineKeyboardButton(text='❌ Отмена', callback_data='continue')
            sub = types.InlineKeyboardButton(text='✅ Продолжить', callback_data='quickmessagesend')
            cancel.add(can, sub)
            bot.send_message(message.chat.id, "<b>Введите срочное сообщение.</b>", parse_mode="HTML",
                             reply_markup=cancel)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


def quickmessagesend(message):
    data = readmembers()
    for i in range(len(data['members'])):
        if str(data['members'][i]['id']) != str(message.chat.id):
            bot.send_message(int(data['members'][i]['id']), "<b>Срочное сообщение!</b>\n" + str(message.text),parse_mode="HTML")
    bot.send_message(message.chat.id, "<b>Срочное сообщение отправлено!</b>\n", parse_mode="HTML",
                     reply_markup=adminkamarkup)


@bot.message_handler(func=lambda message: message.text == "🎖 Ачивки" or message.text == "/editachives")
def handle_editachives(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            cancel = types.InlineKeyboardMarkup(row_width=3)
            can = types.InlineKeyboardButton(text='❌ Отмена', callback_data='continue')
            sub = types.InlineKeyboardButton(text='🏆 Выдать ачивку', callback_data='giveachive')
            delete=types.InlineKeyboardButton(text='♻️ Удалить ачивку', callback_data='deleteachive')
            cancel.add(can)
            cancel.add(sub)
            cancel.add(delete)
            bot.send_message(message.chat.id, "<b>Выберите действие:</b>", parse_mode="HTML", reply_markup=cancel)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


def giveachive(message):
    try:
        data = readmembers()
        text = message.text.split(" ")
        number=int(text[0])
        del text[0]
        text = " ".join(text)
        if number>0 and number<=len(data) and text!='':
                data['members'][int(number)-1]['achives'].append({"name": str(text), "adding": ""})
                markup = types.InlineKeyboardMarkup(row_width=2)
                #add = types.InlineKeyboardButton(text='📎 Добавить файл', callback_data='addition')
                fin = types.InlineKeyboardButton(text='🎗 Выдать ачивку!', callback_data='giveaway')
                #markup.add(add)
                markup.add(fin)
                writemembers(data)
                bot.send_message(message.chat.id,
                                 "<b>Ачивка выдается пользователю с именем: </b>" + str(
                                     data['members'][int(number)-1]['name']) + "\n<b>Название ачивки: </b>" + str(text)
                                 , parse_mode="HTML", reply_markup=markup)
        else:
            send = bot.send_message(message.chat.id,
                                    "<b>Неправильный формат ввода!</b>\n\n<i>Пример:</i>\n1 Не ел вторую неделю?",
                                    parse_mode="HTML")
            bot.register_next_step_handler(send, giveachive)

    except IndexError:
        send=bot.send_message(message.chat.id,"<b>Неправильный формат ввода!</b>\n\n<i>Пример:</i>\n1 Не ел вторую неделю?",parse_mode="HTML")
        bot.register_next_step_handler(send,giveachive)

@bot.message_handler(func=lambda message: message.text == "❌ Выход" or message.text == "/exit")
def exit(message):
    auth = checker(message)
    if auth[0] != 0:
        if auth[0] == 2:
            bot.send_message(message.chat.id, "<b>Вы вышли из административного режима</b>", parse_mode="HTML",
                             reply_markup=adminmarkup)
        else:
            bot.send_sticker(message.chat.id, "CAADAgADQQoAApkvSwqnrw2BEeUQJwI")
    else:
        start(message)


#Квестики ^_^
@bot.message_handler(func=lambda message: message.text == "🎮 Квест" or message.text == "/quest")
def handle_quest(message):
    auth = checker(message)
    if auth[0]!=0:
        quest = readquest()
        #запуск квеста
        if int(quest['quest']) == 1:
            user=activequestion(message)
            if user==0:
                send = bot.send_message(message.chat.id, "Введи логин своей группы, чтобы начать квест!")
                bot.register_next_step_handler(send, questregister)
            else:
                send=bot.send_message(message.chat.id, "<b>Вопрос №"+str(int(user[1])+1)+"</b>\n"+str(user[0]),parse_mode="HTML")
                bot.register_next_step_handler(send, checkquestion)
    else:
        start(message)


def activequestion(message):
    quest=readquest()
    # листаем все группы
    question=0

    for m in range(len(quest['groups'])):
        # листаем всех юзеров в группах
        for j in range(len(quest['groups'][m]['users'])):
            # если юзер нашелся
            if str(message.chat.id) == str(quest['groups'][m]['users'][j]['id']):
                question = ''
                # листаем все вопросы
                for n in range(len(quest["questions"])):
                    # если активный вопрос в группе совпадает с одним из вопросов
                    if str(quest["questions"][n]["id"]) == str(quest['groups'][m]['activequetsion']):
                        question = [quest["questions"][n]['question'],quest["questions"][n]["id"]]
    return question


def questregister(message):
    quest = readquest()
    x=0
    for i in range(len(quest['groups'])):
        if message.text==quest['groups'][i]['password']:
            x=1
            quest['groups'][i]['users'].append({"id":str(message.chat.id)})
            writequest(quest)
            send=bot.send_message(message.chat.id,"<b>Вопрос №1</b>\n"+activequestion(message)[0],parse_mode="HTML")
            bot.register_next_step_handler(send,checkquestion)
    if x==0:
        send = bot.send_message(message.chat.id, "Неправильный логин!", parse_mode="HTML")
        bot.register_next_step_handler(send, questregister)

def checkquestion(message):
    quest=readquest()
    question=activequestion(message)[1]
    right=False
    for i in range(len(quest['questions'])):
        if question==quest['questions'][i]['id']:
            if str(message.text)==str(quest['questions'][i]['answer']):
                right=True
                bot.send_message(message.chat.id,"Правильный ответ!")
                for m in range(len(quest['groups'])):
                    # листаем всех юзеров в группах
                    for j in range(len(quest['groups'][m]['users'])):
                        # если юзер нашелся
                        if str(message.chat.id) == str(quest['groups'][m]['users'][j]['id']):
                            quest['groups'][m]['activequetsion']=int(quest['groups'][m]['activequetsion'])+1
                            question=quest['groups'][m]['activequetsion']
                            writequest(quest)
                            for k in range(len(quest['questions'])):
                                if int(quest['questions'][k]['id'])==question:
                                    text=quest['questions'][k]['question']
                            if len(quest['questions'])==question-1:
                                usermarkup = types.ReplyKeyboardMarkup(True, False)
                                usermarkup.row('🗓 Расписание', '⛳️ Событие')
                                usermarkup.row('🏅 Ачивки', '❗️ Информация')
                                usermarkup.row('🛠 Комманды')
                                for p in range(len(quest['groups'][m]['users'])):
                                    bot.send_message(int(quest['groups'][m]['users'][p]['id']),"Ура! Вы закончили квест!",parse_mode="HTML",reply_markup=usermarkup)
                                quest['groups'][m]['finish']=str(tm.localtime()[3])+":"+str(tm.localtime()[4])+":"+str(tm.localtime()[5])
                                time=quest['groups'][m]['finish']
                                writequest(quest)
                                members=readmembers()['members']
                                for p in range(len(members)):
                                    if int(members[p]['admin'])==2:
                                        bot.send_message(members[p]['id'],"Команда №"+str(m+1)+" закончила квест в "+str(time))
                            else:
                                for p in range(len(quest['groups'][m]['users'])):
                                    send=bot.send_message(int(quest['groups'][m]['users'][p]['id']),"<b>Вопрос №"+str(question)+"</b>\n"+text,parse_mode="HTML")
                                    bot.register_next_step_handler(send,checkquestion)
    if right==False:
        send=bot.send_message(message.chat.id, "Неправильный ответ!")
        bot.register_next_step_handler(send,checkquestion)


@bot.callback_query_handler(func=lambda message: True)
def inline(message):
    if message.data == 'continue':
        bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                              text="<b>Действие было отменено!</b>", parse_mode="HTML")
    elif message.data == "newschedule":
        then = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                     text="<b>Введите расписание в формате:</b>\n08:00 Первое событие\n20:00 Второе событие",
                                     parse_mode="HTML")
        bot.register_next_step_handler(then, newschedule)
    elif message.data == "newadress":
        then = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                     text="<b>Введите новую информацию о проживании.</b>", parse_mode="HTML")
        bot.register_next_step_handler(then, newadress)
    elif message.data == "newphones":
        then = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                     text="<b>Введите новую контактную информацию.</b>", parse_mode="HTML")
        bot.register_next_step_handler(then, newphones)
    elif message.data == "quickmessagesend":
        then = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                     text="<b>Введите срочное сообщение.</b>", parse_mode="HTML")
        bot.register_next_step_handler(then, quickmessagesend)
    elif message.data == "whereilive":
        info = readinfo()['adress']
        if info!='':
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                              text="<b>Информация о проживании.</b>\n\n" + str(info), parse_mode="HTML")
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                  text="<b>Информацию о проживании еще не добавили</b>", parse_mode="HTML")
            bot.send_sticker(message.message.chat.id,"CAADAgADswoAAkKvaQABaMOVR9paPiQC")
    elif message.data == "phones":
        info = readinfo()['info']
        if info!='':
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                              text="<b>Контактная информация.</b>\n\n" + str(info), parse_mode="HTML")
        else:
            bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                  text="<b>Контактную информацию еще не добавили</b>", parse_mode="HTML")
            bot.send_sticker(message.message.chat.id,"CAADAgADswoAAkKvaQABaMOVR9paPiQC")

    elif message.data == "giveachive":
        data = readmembers()['members']
        stroke = ''
        for i in range(1, len(data) + 1):
            if str(data[i - 1]['id']) != message.message.chat.id:
                stroke += str(i) + ". " + str(data[i - 1]['name'])+"\n"
        add = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                    text="<b>Введи номер пользователя, которому ты хочешь выдать ачивку и название ачивки через пробел. </b>\n\n"
                                         + str(stroke), parse_mode="HTML")
        bot.register_next_step_handler(add, giveachive)

    elif message.data == 'deleteachive':
        data = readmembers()['members']
        stroke = ''
        for i in range(1, len(data) + 1):
            if len(data[i-1]['achives'])!=0:
                #if str(data[i - 1]['id']) != str(message.message.chat.id):
                stroke += str(i) + ". " + str(data[i - 1]['name']) + "\n"
        if stroke!='':
            add = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                text="<b>Введи номер пользователя, у которого ты хочешь удалить ачивку!</b>\n\n"
                                     + str(stroke), parse_mode="HTML")
            bot.register_next_step_handler(add, deletelog)
        else:
            add = bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                text="<b>Ни у одного пользователя нет ачивок!</b>\n\n"
                                     + str(stroke), parse_mode="HTML")

    elif message.data == "giveaway":
        text = message.message.text[38:].split("\n")[0]
        data = readmembers()
        for i in range(len(data['members'])):
            if str(text).replace(" ", "") == str(data['members'][i]['name']).replace(" ", ""):
                bot.send_message(int(data['members'][i]['id']),
                                 "<b>Ты получил новую ачивку!\n\nНазвание: </b>" + str(
                                     data['members'][i]['achives'][-1]['name']),
                                 parse_mode="HTML")
                bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      text="<b>Ты выдал ачивку!</b>",
                                      parse_mode="HTML")
    elif message.data == "addition":
        send=bot.send_message(message.message.id,"Пришли файл/стикер/аудиозапись/фото")
        bot.register_next_step_handler(send,addition)

# Бесконечность не предел!
if __name__ == '__main__':
    bot.polling(none_stop=True)