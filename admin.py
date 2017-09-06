# -*- coding: utf-8 -*-
import sqlconnect as sql
import datetime
from datetime import date, time

def notation(message):
    temp = {}
    temp['id'] = message.chat.id
    if message.content_type == 'text':
        temp['dist'] = "Срочная рассылка: \n" + message.text
        temp['id2'] = []
        cur = sql.select("SELECT ChatID FROM main;")
        for row in cur:
            temp['id2'].append(row[0])
        temp['text'] = 'Сообщение успешно разосланно!'
    else:
        temp['text'] = 'Данный формат сообщения не поддерживается.'
    return temp


def add_event(message):
    temp = {}
    temp['id'] = message.chat.id
    msg = message.text.split('\n')
    for data in msg:
        sthour = stminute = finhour = finminute = 0
        data = data.split(" : ")
        if len(data) == 2:
            name = data[0]
            data = data[1]
            data = data.split(' ')
            if len(data) == 6:
                try:
                    year = datetime.datetime.now().year
                    month = int(data[0])
                    day = int(data[1])
                    sthour = int(data[2])
                    stminute = int(data[3])
                    finhour = int(data[4])
                    finminute = int(data[5])
                    d = date(year, month, day)
                except ValueError:
                    temp['text'] = 'Неправильный формат ввода!'
                    return temp
                else:
                    t1 = time(sthour, stminute)
                    t2 = time(finhour, finminute)
                    sql.edit("INSERT INTO timetable (Event, Date, Start, Finish)VALUES('" + name + "', '" + str(
                        d) + "', '" + str(t1) + "', '" + str(t2) + "');")
                    temp['text'] = 'Мероприятие успешно добавленно!'
                    return temp
            else:
                temp['text'] = 'Неправильный формат ввода!'
                return temp
        else:
            temp['text'] = 'Неправильный формат ввода!'
            return temp



def add_trophy(message):
    temp = {}
    temp['id'] = message.chat.id
    msg = message.text.split('\n')
    for data in msg:
        chatid = ''
        data = data.split(' : ')
        if len(data) == 2:
            name = data[0]
            trophy = data[1]
            cur = sql.select("SELECT ChatID FROM main WHERE name='" + name + "';")
            for row in cur:
                chatid = row
            if chatid == '':
                temp['text'] = 'Не удалось найти пользователя! Проверьте формат ввода.'
                return temp
            else:
                chatid = int(chatid[0])
                sql.edit("INSERT INTO trophy (ChatID, Achiev) VALUES (" + str(chatid) + ", '" + trophy + "');")
                temp['text'] = 'Достижение успешно добавлено!'
                temp['id2'] = chatid
                temp['text2'] = 'Вы получили достижение: ' + trophy
                return temp
        else:
            temp['text'] = 'Неправильный формат ввода!'
            return temp


def add_contact(message):
    msg = message.text.split('\n')
    for data in msg:
        sql.edit("INSERT INTO contacts (contact) VALUES ('" + data + "');")


def add_home(message):
    temp = {}
    temp['id'] = message.chat.id
    msg = message.text.split('\n')
    for data in msg:
        chatid = ''
        data = data.split(' : ')
        if len(data) == 2:
            name = data[0]
            home1 = data[1]
            cur = sql.select("SELECT ChatID FROM main WHERE name='" + name + "';")
            for row in cur:
                chatid = int(row[0])
            try:
                sql.edit("UPDATE main SET Home='" + home1 + "' WHERE ChatID=" + str(chatid) + ";")
                temp['text'] = 'Место проживания успешно обновлено.'
                return temp
            except Exception:
                temp['text'] = 'Не удалось найти пользователя! Проверьте формат ввода.'
                return temp
        else:
            temp['text'] = 'Неправильный формат ввода!'
            return temp
