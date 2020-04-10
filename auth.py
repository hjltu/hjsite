
"""
auth.py
"""

import os, sys
import functools
from flask import (
    Blueprint, flash, g, redirect, session,
    render_template, request, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

import myemail
# registration token
import random
symbols = 'abcdefghijkmnpqrstuvwxyz1234567890ABCDEFGHJKMNPRSTUVWXYZ'
# db
db= os.environ['HOME'] + '/instance/user.db'

import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from setup.rpi_serial import ip, hostname

bp = Blueprint(
    'auth', __name__,
    template_folder='templates',
    static_folder='static',)
#    url_prefix='/templates')

def login_required(view):
    @functools.wraps(view)
    def decorated_function(**kwargs):
        #if user == {}:
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return decorated_function


@bp.route("/logout")
def logout():
    session.clear()
    #return render_template("index.html")
    return redirect(url_for("mysite.index"))


@bp.route("/login", methods=('GET', 'POST'))
def login():
    err=None
    if request.method == "POST":
        name = request.form["username"]
        passwd = request.form["password"]

        user = schema.my_login(db, name)
        if user is None:
            err = "Incorrect Username"
        elif not check_password_hash(user['passwd'], passwd):
            err = "Incorrect Password"

        if err is None:
            session.clear()
            session["user_id"] = name
            session["uuid"] = user['uuid']
            #if user['uuid'] != 'CONFIRMED':
                #args = [name, siteName, user['uuid']]
                #myemail.main(args)
            return redirect(url_for(
                "mysite.index", user=name,  err=err))

        #flash(err)

    return render_template("login.html", user=None, err=err)


@bp.route("/register", methods=("GET", "POST"))
def register():
    import re
    err = None
    if request.method == "POST":
        name = request.form["username"]
        passwd = request.form["password"]

        if not name:
            err="Username is required"
        elif not re.match("[^@]+@[^@]+\.[^@]+", name):
            err="Username must be valid email"
        elif not passwd:
            err="Password is required"
        elif len(passwd)<6:
            err="Password is too short"

        if err is None:
            token = ''.join(random.sample(symbols,10))
            res = schema.my_register(
                db, name, generate_password_hash(passwd), token)
            if res is None:
                args = [name, token]
                print('send email',args)
                myemail.main(args)
                return redirect(url_for("auth.login"))
            else:
                err="User {} is already registered".format(name)
                #err = res

        #flash(err)

    return render_template("register.html", err=err)


@bp.route('/settings', methods=('GET', 'POST'))
@login_required
def settings():
    err=None
    tokenStat = ''
    if g.token == 'CONFIRMED':
        tokenStat = g.token
    if request.method == "POST":
        passwd = request.form["password"]
        print('password',passwd)
        user = schema.my_login(db, g.user)
        if user is None:
            err = "Incorrect Username"
        elif not check_password_hash(user['passwd'], passwd):
            err = "Incorrect Password"

        if err is None:
            res = schema.my_delete(db, g.user)
            if res is None:
                session.clear()
                return render_template("login.html", user=None, err=err)
            else:
                err=res
                return redirect(url_for(
                    "mysite.index", user=g.user,  err=err))
    return render_template(
        "settings.html", user=g.user, token=tokenStat, err=err)


@bp.route('/confirm/<token>')
@login_required
def confirm_email(token):
    err = None
    user = g.user
    ip=request.remote_addr
    path="confirm/" + token
    print('ch1')
    if token is not None and token != 'CONFIRMED':
        print('ch2')
        res = schema.my_confirm(db, user, token)
        if res is None:
            print('ch3')
            session.clear()
            return redirect(url_for("mysite.index", user=user, err=err))

    return render_template('404.html', ip=ip, path=path, err='404')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    token = session.get('uuid')
    g.user=user_id
    g.token=token
#    if config.SSL is True:
#        print('ssl1')
#        if request.url.startswith('http://'):
#            print('ssl2')
#            url = request.url.replace('http://', 'https://', 1)
#            code = 301
#            return redirect(url, code=code)
