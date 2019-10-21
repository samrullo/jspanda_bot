import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xf4\xc6\x11t\x94\x86\xaaN#\x8a#\x11=Q\x92\xe1'
