import os
import sys
sys.path.insert(0,'/var/www/jspanda_bot')
from appserver import app as application
application.secret_key = os.environ.get('SECRET_KEY') or b'\xf4\xc6\x11t\x94\x86\xaaN#\x8a#\x11=Q\x92\xe1'