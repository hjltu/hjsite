"""
schema.py
mydb.py
27-may-19 hjltu@ya.ru

users: id, user, pass, uuid, mail, time
bridge: id, user, sn, time
device: id, sn, type, name, comm, stat, time
"""

import mydb



NEW_DB = """
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS bridge;
DROP TABLE IF EXISTS device;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user TEXT UNIQUE NOT NULL,
  pass TEXT NOT NULL,
  uuid TEXT NOT NULL,
  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bridge (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user TEXT NOT NULL,
  sn TEXT UNIQUE NOT NULL,
  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE device (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  rpi TEXT NOT NULL,
  name TEXT UNIQUE NOT NULL,
  comm TEXT NOT NULL,
  stat TEXT NOT NULL,
  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

"""

def my_create(db, query=NEW_DB):
#    return
    res = mydb.my_query(db, query)
    print('*** create db', db, res)


def my_login(db, name):
    query = "SELECT * FROM users WHERE user = '" + name + "';"
    res = mydb.my_query(db, query, True)
    print(res)
    if res:
        if 'ERR' not in res and len(res[0]) == 5:
            user = {}
            user["passwd"]=res[0][2]
            user["uuid"]=res[0][3]
            return user
    return None


def my_register(db, name, passwd, uuid):
    query = "INSERT INTO users (user,pass,uuid) VALUES ('" + \
        name +"', '" + passwd + "', '" + uuid + "');"
    res = mydb.my_query(db, query, True)
    print(res)
    if res == []:
        return None
    else:
        return res

def my_confirm(db, name, uuid):
    if uuid != 'CONFIRM':
        query = "UPDATE users SET uuid = 'CONFIRMED' \
        WHERE user = '" + name + "';"
        res = mydb.my_query(db, query, True)
        print(res)
        if res == []:
            return None
        else:
            return res

def my_delete(db, name):
    query = "DELETE FROM users WHERE user = '" + name + "';"
    res = mydb.my_query(db, query, True)
    print(res)
    if res == []:
        return None
    else:
        return res

def my_bridge(db, name):
    query = "SELECT sn FROM bridge WHERE user = '" + name + "';"
    res = mydb.my_query(db, query, True)
    print(res)

def add_bridge(db, name, sn):
    query = "INSERT INTO bridge (user, sn) VALUES ('" + \
        name + "', '" + sn + "');"
    res = mydb.my_query(db, query, True)
    print(res)







