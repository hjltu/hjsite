#!/usr/bin/env python3
"""
site_setup.py
"""

import os
import socket
import snumber

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "192.168.0.10"
    finally:
        s.close()
    return ip


def get_mac(serial):
    sn = snumber.main(serial)
    mac = "AA:BB:"
    for i in range(0, 8, 2):
        #if str(sn[i+1]) == "0":
        #    mac += str(sn[i])+"1"
        #else:
        mac += str(sn[i])+str(sn[i+1])
        if i<6:
            mac += ':'
    print('mac',mac)
    os.environ['MAC_ADDR'] = mac
    os.system("sudo sed -i 's/AA:BB:CC:DD:EE:FF/"+mac+"/' /etc/systemd/system/hjhome.service")
    return mac


def get_pin(serial):
    sn = snumber.main(serial)
    pin = ''
    for i in range(8):
        pin += str(sn[i])
        if i == 2 or i == 4:
            pin += '-'
    print('pin',pin)
    os.environ['PIN_NUMBER'] = pin
    os.system("sudo sed -i 's/123-45-678/"+pin+"/' /etc/systemd/system/hjhome.service")
    return pin


class Conf(object):
    SECRET_KEY = "mysite"
    SQL_DB = "instance/test.db"
    LOCAL_IP = get_ip()
    SERIAL = get_serial()
    MAC_ADDR = get_mac(SERIAL)
    PIN_NUMBER = get_pin(SERIAL)
    UPLOAD_FOLDER = os.environ['HOME']
    ALLOWED_EXTENSIONS = {'csv'}
    CSV_FILE = SERIAL+".csv"
    MAX_FILE_SIZE = 99999


class Prod(Conf):
    DEBUG = False
    SQL_DB = "instance/mysite.db"
    SQL_ECHO = False


class Dev(Conf):
    DEBUG = True
    #SQL_DB = "sqlite:///:memory:"
    #SQL_DB = ":memory:"
    SQL_ECHO = True
