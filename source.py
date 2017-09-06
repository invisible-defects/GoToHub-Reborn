# -*- coding: utf-8 -*-
from threading import Timer

import telebot
from telebot import types
import feedparser

import config
import markup_kboards as m
import user_check
import admin
import user
import sqlconnect as sql

print(config.token)
bot = telebot.TeleBot(config.token)
#quest_dict = {}
team_dict = {}
admin_quest = {}

kid_password = config.password
admin_password = config.admin
parents_password = config.parents


def event_checker():
    sql.edit("UPDATE timetable SET Active=1 WHERE (Date=CURRENT_DATE() AND CURRENT_TIME() >= Start AND CURRENT_TIME() "
             "<= Finish AND Active = 0);",
             "UPDATE timetable SET Active=0 WHERE (Date!=CURRENT_DATE() OR CURRENT_TIME() "
             "< Start OR CURRENT_TIME() > Finish);")
    cur = sql.select("SELECT Event FROM timetable WHERE Active=1;")
    out = ''
    for row in cur:
        out += str(row[0]) + '\n'
    if out != '':
        sql.edit("UPDATE timetable SET Active=2 WHERE Active=1;")
        cur = sql.select("SELECT ChatID FROM main;")
        for row in cur:
            chatid = str(row[0])
            bot.send_message(int(chatid), 'Началось мероприятие: \n' + out)
    t = Timer(30.0, event_checker)
    t.start()


event_checker()


def addkey(message):
    msg = message.text.split('\n')
    go = True
    for data in msg:
        if data == 'Готово!':
            bot.send_message(message.chat.id, 'Квест успешно создан!', reply_markup=m.markup3)
            go = False
            break
        elif len(data.split(' ')) < 2 and not data.isdigit():
            sql.edit("ALTER TABLE " + admin_quest[message.chat.id] + " ADD " + data + " TINYINT DEFAULT 2;")
            bot.send_message(message.chat.id, 'Ключ добавлен!')
        else:
            bot.send_message(message.chat.id,
                             'Ключ не должен содержать пробелов и состоять не только из цифр! Попробуйте еще раз.')
    if go:
        bot.register_next_step_handler(message, addkey)


def addquestions(message):
    if message.text == 'Готово!':
        bot.send_message(message.chat.id, 'Теперь добавьте ключи команд. Для каждый команды, участвующей в конкурсе '
                                          'придумайте собственный идентификатор, состоящий из одного слова. '
                                          'Вы можете отправить несколько идентификаторов в одном сообщении, '
                                          'начиная каждый последующий с новой строки. '
                                          'Когда закончите, отправьте "Готово!"')
        bot.register_next_step_handler(message, addkey)
    else:
        msg = message.text.split('\n')
        for data in msg:
            try:
                data = data.split(' : ')
                question = data[0]
                answer = data[1]
            except IndexError:
                bot.send_message(message.chat.id, 'Неверный формат вопроса. Введите вопрос еще раз.')
            else:
                sql.edit(
                    "INSERT INTO " + admin_quest[
                        message.chat.id] + " (Question, Answer) VALUES ('" + question + "', '" + answer + "');")
                bot.send_message(message.chat.id, 'Вопрос добавлен!')
        bot.register_next_step_handler(message, addquestions)


def newquest(message):
    if len(message.text.split(' ')) > 1:
        bot.send_message(message.chat.id, 'Неправильный формат ввода! Не используйте пробелы.', reply_markup=m.markup3)
    else:
        questname = 'quest_' + message.text
        try:
            admin_quest.update({message.chat.id: questname})
            sql.edit(
                "CREATE TABLE " + questname + " (Question VARCHAR(255) NOT NULL, Answer VARCHAR(255) NOT NULL ) "
                                              "ENGINE=InnoDB;")
            bot.send_message(message.chat.id, 'Далее введите вопросы и ответы квеста в формате: "Вопрос : Ответ". \n '
                                              'Пример: '
                                              '\n "Продолжите фразу - программисты не рождаются, программисты... : '
                                              'Наследуются"\n Вы можете отправить несколько вопросов в одном сообще'
                                              'нии, начиная каждую новую пару с новой строки. '
                                              'Когда закончите, отправьте "Готово!"')
            bot.register_next_step_handler(message, addquestions)
        except Exception:
            bot.send_message(message.chat.id, 'Такой квест уже существует.', reply_markup=m.markup3)


def admin_notice(message):
    temp = admin.notation(message)
    for idis in temp['id2']:
        bot.send_message(idis, temp['dist'])
    bot.send_message(temp['id'], temp['text'], reply_markup=m.markup3)


def admin_add_event(message):
    temp = admin.add_event(message)
    bot.send_message(temp['id'], temp['text'], reply_markup=m.markup3)


def admin_add_trophy(message):
    temp = admin.add_trophy(message)
    bot.send_message(temp['id'], temp['text'], reply_markup=m.markup3)
    if 'id2' in temp:
        bot.send_message(temp['id2'], temp['text2'])


def admin_add_contact(message):
    admin.add_contact(message)
    bot.send_message(message.chat.id, 'Контакт добавлен!', reply_markup=m.markup3)


def admin_add_home(message):
    temp = admin.add_home(message)
    bot.send_message(temp['id'], temp['text'], reply_markup=m.markup3)


def adminlog(message):
    if message.text == m.smilemeropadmin:
        bot.send_message(message.chat.id, 'Введите сообщение для рассылки:', reply_markup=m.hide)
        bot.register_next_step_handler(message, admin_notice)

    elif message.text == m.smiletrophyadmin:
        bot.send_message(message.chat.id, 'Введите получателя достижения, а затем наименование достижения в формате: \n'
                                          'Полное_Имя Фамилия : Название и описание достижения \n Пример: \n'
                                          '"Василий Пупкин : Костыли - наше Всё"\n'
                                          'Вы можете ввести несколько пар в одном сообщении, начиная каждую'
                                          ' с новой строки.', reply_markup=m.hide)
        bot.register_next_step_handler(message, admin_add_trophy)

    elif message.text == m.smileclockadmin:
        bot.send_message(message.chat.id,
                         'Введите информацию о мероприятии в формате: \n "Название и описание : Месяц День'
                         ' Часы_Начала Минуты_Начала Часы_Конца Минуты_Конца" \n Пример: \n "Самый важный'
                         ' сбор : 3 8 12 15 12 30"\n'
                         'Вы можете ввести несколько меорпиятий в одном сообщении'
                         ', начиная ввод каждого с новой строки.', reply_markup=m.hide)
        bot.register_next_step_handler(message, admin_add_event)

    elif message.text == m.robosmileadmin:
        bot.send_message(message.chat.id, 'Введите и запомните идентификатор квеста. Он должен состоять '
                                          'из одного слова.', reply_markup=m.hide)
        bot.register_next_step_handler(message, newquest)

    elif message.text == m.smileaddcontacts:
        bot.send_message(message.chat.id, 'Введите свои контакты в удобной для вас форме. Не более 255 символов.'
                                          ' \n Пример: \n'
                                          'Василий Пупкин - пионер 1 отряда, +7-999-999-99-99 \n'
                                          'Вы можете ввести несколько контактов в одном сообщении,'
                                          ' начиная каждый с новой строки.', reply_markup=m.hide)
        bot.register_next_step_handler(message, admin_add_contact)

    elif message.text == m.smileaddhome:
        bot.send_message(message.chat.id, 'Введите место проживания пионера в формате: \n'
                                          'Полное_Имя Фамилия : Место жительства \n'
                                          'Пример: \n'
                                          'Василий Пупкин : Главный корпус, комната 209 \n'
                                          'Вы можете ввести несколько пар в одном сообщении, начиная каждую '
                                          'пару с новой строки.', reply_markup=m.hide)
        bot.register_next_step_handler(message, admin_add_home)

    elif message.text == 'Я тут?':
        bot.send_message(message.chat.id, 'Вы в админке')


def playquest(message):
    if message.content_type == 'text' and not (
                                    message.text == m.robosmile or message.text == m.smilepodmig or message.text == m.smiletrophy or message.text == m.smileclock or message.text == m.smilereg or message.text == m.smilemerop):
        cur = sql.select("SELECT " + team_dict[message.chat.id] + " FROM quest WHERE Answer='" + message.text + "';")
        out = ''
        for row in cur:
            out += str(row[0])
            break
        if out == '' or out == '1':
            bot.send_message(chat_id=message.chat.id,text="Неправильный ответ на вопрос!", reply_markup=m.markup4)
            bot.register_next_step_handler(message, playquest)
        else:
            sql.edit("UPDATE quest SET " + team_dict[message.chat.id] + "=1 WHERE " +
                     team_dict[message.chat.id] + "=2 AND Answer='" + message.text + "' LIMIT 1;")
            bot.send_message(chat_id=message.chat.id, text="Ответ верный. Браво!", reply_markup=m.markup4)
            bot.register_next_step_handler(message, playquest)


def continuequest(message):
    teamid = message.text
    if message.text == '2':
        bot.send_message(message.chat.id, 'Неправильный ключ квеста\команды!', reply_markup=m.markup2)
    else:
        team_dict.update({message.chat.id: teamid})
        try:
            cur = sql.select(
                "SELECT Question FROM quest WHERE " + team_dict[message.chat.id] + "=2;")
            out = ''
            for row in cur:
                out += str(row[0])
                break
            if out == '':
                bot.send_message(message.chat.id, 'Квест был пройден ранее!', reply_markup=m.markup2)
            else:
                bot.send_message(message.chat.id,
                                 'Для начала и для получения последующих вопросов, нажмите "Следующий вопрос!". '
                                 'Для выхода, нажмите "Выход!".',
                                 reply_markup=m.markup4)
            bot.register_next_step_handler(message, playquest)
        except Exception:
            bot.send_message(message.chat.id, 'Неправильное имя команды!', reply_markup=m.markup2)


#def startquest(message):
#    questid = "quest_" + message.text
#    quest_dict.update({message.chat.id: questid})
#    bot.send_message(message.chat.id, 'Введите идентификатор команды.')
#    bot.register_next_step_handler(message, continuequest)


def userlog(message):
    if message.text == m.smiletrophy:
        out = user.achievements(message.chat.id)
        bot.send_message(message.chat.id, out,  parse_mode="HTML")

    elif message.text == m.smilemerop:
        out = user.events()
        bot.send_message(message.chat.id, out, parse_mode="HTML")

    elif message.text == m.smileclock:
        out = user.timetable()
        bot.send_message(message.chat.id, out, parse_mode="HTML")

    elif message.text == m.robosmile:
        bot.send_message(message.chat.id, 'Введите название вашей команды!',
                         reply_markup=m.hide)
        bot.register_next_step_handler(message, continuequest)

    elif message.text == m.smilepodmig:
        bot.send_message(message.chat.id, 'Выберите раздел!', reply_markup=m.markup5, parse_mode="HTML")

    elif message.text == m.smilephone:
        bot.send_message(message.chat.id, user.contacts(), reply_markup=m.markup2, parse_mode="HTML")

    elif message.text == m.smilehome:
        bot.send_message(message.chat.id, user.housing(message.chat.id), reply_markup=m.markup2, parse_mode="HTML")

    elif message.text == m.questions:
        bot.send_message(message.chat.id, '<b>Помогите нам улучшить бота!<b> \n'
                                          'Мы тестируем систему автоматического поиска ответа на Ваши вопросы. Если '
                                          'Вы хотите её опробовать, нажмите на галочку. Чтобы найти ответ на вопрос '
                                          'вручную, нажмите на крестик.', reply_markup=m.selection_markup, parse_mode="HTML")
    elif message.text == m.territory:
        bot.send_photo(message.chat.id, 'http://www.ivolga-activ.ru/images/news/ivolga_map_big.jpg')

    elif message.text == 'Я тут?':
        bot.send_message(message.chat.id, 'Вы в юзере', parse_mode="HTML")


def parentlog(message):
    if message.text == m.vk:
        bot.send_message(message.chat.id, 'Группа лагеря ВКонтакте:\n https://vk.com/goto_msk')

    elif message.text == m.smilepodmig:
        out = user.contacts()
        bot.send_message(message.chat.id, out, parse_mode="HTML")

    elif message.text == m.smileclock:
        out = user.timetable()
        bot.send_message(message.chat.id, out, parse_mode="HTML")

    elif message.text == m.territory:
        bot.send_photo(message.chat.id, 'http://www.ivolga-activ.ru/images/news/ivolga_map_big.jpg')

    elif message.text == m.questions:
        bot.send_message(message.chat.id, '<b>Помогите нам улучшить бота!<b> \n'
                                          'Мы тестируем систему автоматического поиска ответа на Ваши вопросы. Если '
                                          'Вы хотите её опробовать, нажмите на галочку. Чтобы найти ответ на вопрос '
                                          'вручную, нажмите на крестик.', reply_markup=m.selection_markup)


def adddata(message):
    if message.content_type == 'text':
        cur = sql.select("SELECT ChatID FROM  main WHERE Name='" + message.text + "';")
        out = ''
        for row in cur:
            out += str(row[0])
            break
        if out == '':
            sql.edit(
                "INSERT INTO main (ChatID, Name) VALUES(" + str(message.chat.id) + ", '" + message.text + "');")
            bot.send_message(message.chat.id, 'Спасибо за регистрацию! Добро Пожаловать в GoTo Hub!',
                             reply_markup=m.markup2)
        else:
            bot.send_message(message.chat.id, 'Такой пользователь уже существует!',
                             reply_markup=m.markup)


# Проверка пароля
def passwordlog(message):
    global kid_password
    global parents_password
    global admin_password

    if message.text == kid_password:
        bot.send_message(message.chat.id,
                         'Великолепно! Теперь введите ваше полное имя, а затем - фамилию. ВАЖНО: соблюдайте порядок,'
                         ' вводите сначала ПОЛНОЕ имя, а потом - фамилию. \n Пример: '
                         'Василий Пупкин',parse_mode="HTML")
        bot.register_next_step_handler(message, adddata)

    elif message.text == admin_password:
        bot.send_message(message.chat.id, 'Добро пожаловать в администрирование GoTo Hub!', reply_markup=m.markup3, parse_mode="HTML")

        sql.edit("INSERT INTO admin (ChatID, Status) VALUES(" + str(message.chat.id) + ", 1);")

    elif message.text == parents_password:
        bot.send_message(message.chat.id, 'Добро пожаловать в GoTo Hub! Здесь будут выкладываться'
                                          ' фотографии и объявления для родителей. '
                                          'Так же вы можете ознакомиться с расписанием дня'
                                          ' пионеров на сегодня и узнать номера телефонов '
                                          'вожатых лагеря.', reply_markup=m.markup6)

        sql.edit("INSERT INTO Parents (ChatID, Status) VALUES(" + str(message.chat.id) + ", 1);")

    else:
        bot.send_message(message.chat.id, '<b>Пароль неверный! </b>Попробуйте еще раз.', reply_markup=m.markup, parse_mode="HTML")


@bot.message_handler(content_types=['photo'])
def photos(message):
    if user_check.check_admin(message.chat.id):
        cur = sql.select("SELECT ChatID FROM Parents;")
        for row in cur:
            chatid = str(row[0])
            bot.forward_message(chatid, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Фотография успешно разослана!')

@bot.message_handler(commands=["start"])
def messagestart(message):
    if user_check.check_admin(message.chat.id):
        id = message.chat.id
        cur = sql.select("SELECT * FROM admin WHERE `ChatID` = " + str(id) + ";")
        for row in cur:
            name = row[1]
        bot.send_message(message.chat.id, "Добро пожаловать, вожатый!", reply_markup=m.markup3)
    elif user_check.check_kid(message.chat.id):
        id = message.chat.id
        cur = sql.select("SELECT * FROM main WHERE `ChatID` = "+str(id)+";")
        for row in cur:
            name = row[1]
        bot.send_message(message.chat.id, "Привет,"+name+", добро пожаловать в лагерь GoTo Camp!", reply_markup=m.markup2)

    elif user_check.check_parent(message.chat.id):
        id = message.chat.id
        cur = sql.select("SELECT * FROM parents WHERE `ChatID` = " + str(id) + ";")
        bot.send_message(message.chat.id, "Приветствую тебя, дорогой родитель! Добро пожаловать в лагерь GoTo Camp!",
                         reply_markup=m.markup2)
    else:
        bot.send_message(message.chat.id, "Вас приветствует лагерь GoTo Camp! Чтобы продолжить, "
                                          "зарегистрируйтесь!", reply_markup=m.markup)

@bot.message_handler(commands=["leave"])
def leave(message):
    if user_check.check_admin(message.chat.id):
        id = message.chat.id
        stroke = "DELETE FROM `admin` WHERE `ChatID` = " + str(id) + ";"
        cur = sql.edit(stroke)
        bot.send_message(message.chat.id, "Ты уже уходишь... Возвращайся ещё!", reply_markup=m.hidemarkup)
        bot.send_sticker(message.chat.id, "CAADAgADdwoAAkKvaQABg_wS9u8cP_kC")
    elif user_check.check_kid(message.chat.id):
        id = message.chat.id
        cur = sql.edit("DELETE FROM main WHERE `ChatID` = " + str(id) + ";")
        bot.send_message(message.chat.id, "Ты уже уходишь... Возвращайся ещё!", reply_markup=m.hidemarkup)
        bot.send_sticker(message.chat.id, "CAADAgADdwoAAkKvaQABg_wS9u8cP_kC")
    elif user_check.check_parent(message.chat.id):
        id = message.chat.id
        cur = sql.edit("DELETE FROM parents WHERE `ChatID` = " + str(id) + ";")
        bot.send_message(message.chat.id, "Ты уже уходишь... Возвращайся ещё!", reply_markup=m.hidemarkup)
        bot.send_sticker(message.chat.id, "CAADAgADdwoAAkKvaQABg_wS9u8cP_kC")

@bot.message_handler(func=lambda message: (message.content_type == 'text'))
def start(message):
    if user_check.check_admin(message.chat.id):
        adminlog(message)
    elif user_check.check_kid(message.chat.id):
        userlog(message)
    elif user_check.check_parent(message.chat.id):
        parentlog(message)
    else:
        if message.text == m.smilereg:
            bot.send_message(message.chat.id, "Введите пароль, сообщенный вам вожатыми!", reply_markup=m.hide)
            bot.register_next_step_handler(message, passwordlog)

@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    if c.data == 'next':
        cur = sql.select(
            "SELECT Question FROM quest WHERE " + team_dict[c.message.chat.id] + "=2;")
        out = ''
        for row in cur:
            out += row[0]
            break
        if out == '':
            bot.send_message(chat_id=c.message.chat.id, text="Поздравляем, вы прошли квест!", reply_markup=m.markup2)
            cur = sql.select("SELECT ChatID FROM admin;")
            for row in cur:
                chatid = str(row)
                chatid = chatid[1:-2]
                bot.send_message(int(chatid), "Команда " + team_dict[c.message.chat.id] + " прошла квест!")

        else:
            if not out == c.message.text:
                bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text=out, reply_markup=m.markup4)

    elif c.data == 'ext':
        bot.edit_message_text(chat_id=c.message.chat.id,message_id=c.message.message_id, text='Вы вышли из квеста.')
        bot.send_message(chat_id=c.message.chat.id, text='Вы снова в меню!', reply_markup=m.markup2)

    elif c.data == 'text_faq':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=m.categ,
                              text='Выберите категорию!')
        #bot.send_message(c.message.chat.id, 'Выберите категорию!', reply_markup=m.categ)
    elif c.data == 'faq_about':
        new_button = types.InlineKeyboardButton(text=line[0], callback_data='faq_' + line[1])
        new_keyb.add(new_button)
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, reply_markup=m.categ,
                              text='Выберите категорию!')
    elif c.data == 'neuro_faq':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Эта функция еще не готова! :c')

    elif 'faq_' in c.data:
        cur = sql.select("SELECT link FROM faq_db WHERE inline_data ='" + c.data[4:] + "';")
        for row in cur:
            next_link = row[0]
            break
        cur = sql.select("SELECT link FROM faq_db WHERE adress ='" + next_link + "';")
        for row in cur:
            following_link = row[0]
    #        break
        if following_link == 'stop':
            cur = sql.select("SELECT text FROM faq_db WHERE adress ='" + next_link + "';")
            for row in cur:
                answer = row[0]
                break
            bot.send_message(c.message.chat.id, '*' + answer + '*', parse_mode='markdown')
        else:
            new_markup = sql.select("SELECT text, inline_data FROM faq_db WHERE adress ='" + next_link + "';")
            new_keyb = types.InlineKeyboardMarkup()
            for line in new_markup:
                new_button = types.InlineKeyboardButton(text=line[0], callback_data='faq_' + line[1])
                new_keyb.add(new_button)
            bot.send_message(c.message.chat.id, 'Выберите подкатегорию!', reply_markup=new_keyb)


if __name__ == '__main__':
    bot.polling(none_stop=True)
