# -*- coding: utf-8 -*-
import sqlconnect as sql

def check_kid(chatid):
    cur = sql.select("SELECT Name FROM main WHERE ChatID=" + str(chatid) + ";")
    out = ""
    for row in cur:
        out += str(row)
    if out == '':
        return False
    else:
        return True


def check_admin(chatid):
    cur = sql.select("SELECT Status FROM admin WHERE ChatID=" + str(chatid) + ";")
    out = ""
    for row in cur:
        out += str(row[0])
        break
    if out == '':
        return False
    else:
        return True


def check_parent(chatid):
    cur = sql.select("SELECT Status FROM parents WHERE ChatID=" + str(chatid) + ";")
    out = ""
    for row in cur:
        out += str(row[0])
        break
    if out == '':
        return False
    else:
        return True