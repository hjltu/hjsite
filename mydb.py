#!/usr/bin/env python3

"""
mydb.py
27-may-19 hjltu@ya.ru

usage:
import mydb
import schema
from instance.config import Dev as config
mydb.my_query(config.SQL_DB, schema.NEW_DB)

"""

import sqlite3


def my_query(name, query, verbose=False):
    """ execute any sqlite3 query """


    if verbose == True:
        print('create db in:', name,'\nquery:',query)

    db=sqlite3.connect(name)
    cur=db.cursor()
    try:
        for q in query.split(";"):
            if len(q)>1:
                cur.execute(q)
    except Exception as e:
        db.rollback()
        return "ERR: "+ str(e)
    rows=cur.fetchall()
    if verbose == True:
        print('res',rows)
    #rows=my_retype(rows)
    db.commit()
    db.close()
    return rows


def my_retype(listIn):
    """ input: [(n,),]
        output: [] """

    #  if one element in listIn then return list
    if type(listIn) == 'list' and len(listIn)==1:
        return [listIn[0][el] for el in range(len(listIn[0]))]
    else:
        return 'ERR: empty output'

def my_example():
    """ schema from file"""

    db=sqlite3.connect(name)
    cur=db.cursor()
    with open('schema.sql') as fp:
        cur.executescript(fp.read())


