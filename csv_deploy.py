#!/usr/bin/env python3
"""
csv_depliy.py
hjltu@ya.ru
27-jul-19 create
"""

import os
import csv
from instance.config import Dev as config
import csv2list


CSV_FILE = config.SERIAL + '.csv'
CSV_PATH = config.UPLOAD_FOLDER


def check_csv_file_exist():
    files = os.listdir(CSV_PATH)
    if CSV_FILE in files:
        return True


def create_csv_file(csvfile):
    """
    input: csv file name
    """
    os.system('cp ' + CSV_PATH + '/file.csv '+csvfile)


def parse_csv_file(csvfile):
    """
    input: csv file
    output: list of dicts
    """
    return csv2list.main(csvfile)


def json_file_gen(acc):
    """
    exec filegen.sh to create
        json file homekit accessory
    """
    acc_prop=''
    for a in acc:
        acc_prop += a["type"]+' '+a["acc"]+' '+a["name"]+' '
    print('acc_prop:', acc_prop)
    #return os.system("./new-filegen.sh " + acc_prop)
    return os.system("./filegen.sh " + acc_prop)


def main():
    """
    return True if everything is OK
        or error string
    system env variables:
        read:
            home = os.environ['HOME']
            sn = os.getenv('SERIAL', '1234abcd')
        write:
            os.environ['SERIAL'] = '1234abcd'
    """
    if check_csv_file_exist() is not True:
        create_csv_file(CSV_PATH + '/' + CSV_FILE)
        if check_csv_file_exist() is not True:
            return "file {} not found in {}".format(CSV_FILE, CSV_PATH)
    acc = parse_csv_file(CSV_PATH + '/' + CSV_FILE)
    if type(acc) is 'str':
        return acc
    res = json_file_gen(acc)
    print('res',res)
    if res != 0:
        print('check')
        return "ERR filegen"
    home = os.environ['HOME']
    print('bash '+home + '/ns.sh')
    os.system('bash '+home + '/ns.sh &')
    return True


if __name__ == "__main__":
    main()
