# -*- coding: utf-8 -*-
import sqlconnect as sql

def achievements(id):
    out = "<b>Список ваших достижений:</b>\n\n"
    cur = sql.select("SELECT Achiev FROM trophy WHERE ChatID=" + str(id) + ";")
    for row in cur:
        out += row[0] + "\n"
    if out == "<b>Список ваших достижений:</b>\n\n":
        return '<b>У вас пока нет достижений!</b>'
    else:
        return out

def events():
    cur = sql.select("SELECT Event FROM timetable WHERE Active=2;")
    out = ''
    for row in cur:
        out += str(row[0])
        out += '\n'
    if out == '':
        return '<b>На данный момент нет активных мероприятий.</b>'
    else:
        return '<b>Сейчас проходит мероприятие:</b>\n\n' + out

def timetable():
    cur = sql.select("SELECT Start, Event, Active FROM timetable WHERE Date=CURRENT_DATE() ORDER BY Start;")
    out = ''
    for row in cur:
        if row[2] == 0:
            out += chr(0x2705)+'  '
        elif row[2] == 2:
            out += chr(0x2611) + '  '
        else:
            out += chr(0x274E) + '  '
        out += str(row[0])[:-3] + ' - ' + str(row[1])+ '\n'
    if out == '':
        return '<b>На сегодня мероприятий не залпанировано!</b>'
    else:
        return '<b>Мероприятия на сегодня:</b>\n\n' + out

def contacts():
    cur = sql.select("SELECT contact FROM contacts;")
    out = '<b>Контакты вожатых:</b>\n \n'
    for row in cur:
        out += row[0] + '\n'
    return out

def housing(id):
    cur = sql.select("SELECT Home FROM main WHERE ChatID=" + str(id) + ";")
    out = ''
    for row in cur:
        out += str(row[0])
    if out == 'None':
        return '<b>Ваше место проживания пока не указанно! Попросите об этом вожатых.</b>'
    else:
        return out
