# -*- coding: utf-8 -*-
from telebot import types

robosmile = 'Квесты ' + chr(0x1F916)
smilepodmig = 'Контакты ' + chr(0x1F609)
smiletrophy = 'Достижения ' + chr(0x1F3C6)
smileclock = 'Расписание ' + chr(0x1F557)
smilereg = 'Регистрация ' + chr(0x1F4DD)
smilemerop = 'Что сейчас? ' + chr(0x1F514)
smilephone = 'Телефоны ' + chr(0x1F4DE)
smilehome = 'Где я живу? ' + chr(0x1F3E0)
questions = 'Вопросы ' + chr(0x1F514)

robosmileadmin = 'Создание Квеста ' + chr(0x1F916)
smileclockadmin = 'Задать Расписание ' + chr(0x1F557)
smilemeropadmin = 'Срочное Сообщение ' + chr(0x1F514)
smiletrophyadmin = 'Добавить Достижение ' + chr(0x1F3C6)
smileaddcontacts = 'Добавить Контакт ' + chr(0x1F609)
smileaddhome = 'Место проживания ' + chr(0x1F3E0)
vk = 'Группа лагеря ВКонтакте ' + chr(0x1F5A5)
territory = 'Схема территории ' + chr(0x1F6E3)

hide = types.ReplyKeyboardRemove()

# Интерфейс меню регистрации
markup = types.ReplyKeyboardMarkup()
item = types.KeyboardButton(smilereg)
markup.row(item)

# Юзерский интерфейс
markup2 = types.ReplyKeyboardMarkup()
item2 = types.KeyboardButton(smileclock)
item3 = types.KeyboardButton(smiletrophy)
item4 = types.KeyboardButton(robosmile)
item5 = types.KeyboardButton(smilepodmig)
item11 = types.KeyboardButton(smilemerop)
item13 = types.KeyboardButton(questions)
b_territory = types.KeyboardButton(territory)
markup2.row(item2, item11)
markup2.row(item3, item4)
markup2.row(item5, item13)
markup2.row(b_territory)

# Интерфейс админки
markup3 = types.ReplyKeyboardMarkup()
item6 = types.KeyboardButton(smileclockadmin)
item9 = types.KeyboardButton(smilemeropadmin)
item7 = types.KeyboardButton(smiletrophyadmin)
item8 = types.KeyboardButton(robosmileadmin)
item10 = types.KeyboardButton(smileaddcontacts)
item12 = types.KeyboardButton(smileaddhome)
markup3.row(item6, item9)
markup3.row(item7, item8)
markup3.row(item10, item12)

# Интерфейс кветса
markup4 = types.InlineKeyboardMarkup()
nextq = types.InlineKeyboardButton(text='Следующий вопрос!', callback_data='next')
ext = types.InlineKeyboardButton(text='Выход!', callback_data='ext')
markup4.add(nextq, ext)

# Интерфейс выбора нейро-faq\text-faq
selection_markup = types.InlineKeyboardMarkup()
yes = types.InlineKeyboardButton(text=chr(0x2705), callback_data='neuro_faq')
no = types.InlineKeyboardButton(text=chr(0x274E), callback_data='text_faq')
selection_markup.add(yes, no)

# Категории FAQ
categ = types.InlineKeyboardMarkup()
about = types.InlineKeyboardButton(text='О проекте', callback_data='faq_about')
common = types.InlineKeyboardButton(text='Общее о летнем GoTo Camp', callback_data='faq_common')
vectors = types.InlineKeyboardButton(text='Образовательные направления GoTo Camp', callback_data='faq_vectors')
categ.add(about)
categ.add(common)
categ.add(vectors)

# Интерфейс контактов
markup5 = types.ReplyKeyboardMarkup()
phones = types.KeyboardButton(smilephone)
home = types.KeyboardButton(smilehome)
markup5.row(phones, home)

# Родительский интерфейс
markup6 = types.ReplyKeyboardMarkup()
cntct = types.KeyboardButton(smilepodmig)
rasp = types.KeyboardButton(smileclock)
vkont = types.KeyboardButton(vk)
markup6.row(cntct, rasp)
markup6.row(vkont, item13)
markup6.row(b_territory)

#Спрячем ка интерфейс
hidemarkup = types.ReplyKeyboardRemove()

