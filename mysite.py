
"""
mysite.py
"""

import os

from flask import (
    Blueprint, flash, g, redirect,
    render_template, request, url_for,
    send_from_directory, send_file
)

from werkzeug import secure_filename
from werkzeug.exceptions import abort

from auth import login_required, db

import schema

import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from setup.rpi_serial import serial, pin, ip

ALLOWED_EXTENCIONS = {'csv'}
UPLOAD_FOLDER = os.environ['HOME']+'/config'
CSV_FILE = serial + '.csv'

bp = Blueprint(
    'mysite', __name__,
    template_folder='templates',
    static_folder='static',)

user = {}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/")
@bp.route("/index")
@login_required
def index(err=None, msg=None):
    tokenStat = ''
    if g.token == 'CONFIRMED':
        tokenStat = g.token
    return render_template(
        "index.html", user=g.user, token=tokenStat,
        serial=serial, pin=pin, msg=msg, err=err)


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
    err = None
    msg = None
    tokenStat = ''
    if g.token == 'CONFIRMED':
        tokenStat = g.token
    if request.method == 'POST':
        f = request.files['file']
        #f.save(secure_filename(f.filename))
        filename = secure_filename(f.filename)
        print(allowed_file(filename))
        if f and allowed_file(filename):
            #print('filename', os.path.join(config.UPLOAD_FOLDER, filename))
            f.save(os.path.join(UPLOAD_FOLDER, filename))
            #return 'file uploaded successfully'
            #return redirect(url_for('mysite.index'))
            msg = "file {} upload successfully".format(filename)
            #return index(msg=f"file {filename} upload successfully")
        else:
            err = "file {} not uploaded".format(filename)
            #return index(msg=f"file {filename} not uploaded")

    return render_template(
        'index.html', user=g.user, token=tokenStat,
        serial=serial, pin=pin, msg=msg, err=err)


@bp.route('/download')
@login_required
def download():
    try:
        return send_file(
            UPLOAD_FOLDER+"/"+CSV_FILE,
            as_attachment=True)
    except Exception as e:
        print(e)
        return index(err="File not found. Try to apply")


@bp.route('/apply')
@login_required
def apply():
    if g.token == 'CONFIRMED':
        out = True
        print('apply new csv file')
        print("start script to restart containers")
        out = os.system("sh docker-restart.sh &")
    else:
        return index(err="Not confirmed registration")
    if out != 0:
        return index(err="ERR: restart command returned: {}".format(out))
    return index(msg="send command to restart system, wait about a minute")


@bp.route("/favicon.ico")
def get_favicon():
    return send_from_directory(bp.static_folder,
        'flash.png',mimetype='image/vnd.microsoft.icon')


# all other path
@bp.route("/<path:path>")
def page_not_found(path):
    #ip=request.remote_addr
    return render_template('404.html', ip=ip, path=path, err='404')


