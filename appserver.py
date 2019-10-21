from flask import Flask
from flask import render_template
from flask import request
import os
from flask import session
import json
import logging
from conf.appconf import Config
from controllers.received_money_controller import ReceivedMoneyController

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
_logger = logging.getLogger(__file__)

app = Flask(__name__)
app.config.from_object(Config)
logging.info(f"my secret key is {app.config['SECRET_KEY']}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/show_received_money')
def show_received_money():
    received_money_obj = ReceivedMoneyController()
    return received_money_obj.show_all_received_money()


@app.route('/received_money_add', methods=['GET', 'POST'])
def received_money_add():
    received_money_obj = ReceivedMoneyController()
    return received_money_obj.received_money_add()


@app.route('/received_money_remove/<id>')
def received_money_remove(id=None):
    received_money_obj = ReceivedMoneyController()
    return received_money_obj.received_money_remove(id)


@app.route('/fx')
def fx():
    return render_template("fxcalc.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')