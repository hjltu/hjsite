"""
site
26-may-19

! add instance/ line to .gitignore
curl http://127.0.0.1:5000
"""

import os, sys, time
from flask import Flask

# rate limit
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

# GET POST
from flask import request

# routes
#from flask import redirect, g
#from flask_login import login_required, current_user

# development
#from instance.config import Dev as config
#from instance.config import Prod as config

print("*** START ***")
print('***',os.getcwd())

app = Flask("__name__")
#app=Flask("__name__", instance_relative_config=True)

#app.config.from_object("config")  # if relative = False
#app.config.from_pyfile("config.py")  # load from instance/ if relative = True
#app.config = config

# import Blueprint
import auth
app.register_blueprint(auth.bp)

import mysite
app.register_blueprint(mysite.bp)


# import Blueprint
#import auth
#app.register_blueprint(auth.bp)

#import mysite
#app.register_blueprint(mysite.bp)


if __name__=="__main__":
    app.secret_key = config.SECRET_KEY
    app.debug = config.DEBUG
    app.run(host="0.0.0.0", port=5000)
