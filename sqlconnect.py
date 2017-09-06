# -*- coding: utf-8 -*-
import pymysql


def edit(*commands):
    conn = pymysql.connect(host='localhost', user='shtirlets_goto', passwd='school', db='shtirlets_goto',
                           charset='utf8mb4')
    cur = conn.cursor()
    for command in commands:
        cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()


def select(command):
    conn = pymysql.connect(host='localhost', user='shtirlets_goto', passwd='school', db='shtirlets_goto',
                           charset='utf8mb4')
    cur = conn.cursor()
    cur.execute(command)
    data = cur
    cur.close()
    conn.close()
    return data