import os
import sys
from flask_wtf.csrf import CSRFProtect
import logging

sys.path.insert(0,'/var/www/jspanda_bot')
from appserver import app as application
application.secret_key = os.environ.get('SECRET_KEY') or b'\xf4\xc6\x11t\x94\x86\xaaN#\x8a#\x11=Q\x92\xe1'
csrf = CSRFProtect(app)
logging.info(f"application secret key is {application.secret_key}")
csrf.init_app(app)