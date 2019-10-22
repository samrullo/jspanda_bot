from flask import Flask
from flask import render_template
from flask import request
import os
from flask import session
import json
import logging
from conf.appconf import Config
from controllers.received_money_controller import ReceivedMoneyController
from controllers.family_spending_controller import FamilySpendingController

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


@app.route('/received_money_edit/<id>', methods=['GET', 'POST'])
def received_money_edit(id=None):
    received_money_obj = ReceivedMoneyController()
    return received_money_obj.received_money_edit(id)


@app.route("/family_spending")
def family_spending():
    family_spending_obj = FamilySpendingController()
    return family_spending_obj.family_spending_main()


@app.route("/family_spending_by_month/<month>")
def family_spending_by_month(month):
    family_spending_obj = FamilySpendingController()
    return family_spending_obj.family_spending_month(month)


@app.route("/family_spending_add")
def family_spending_add():
    family_spending_obj = FamilySpendingController()
    return family_spending_obj.family_spending_add()


@app.route("/family_spending_edit/<id>", methods=['GET', 'POST'])
def family_spending_edit(id=None):
    family_spending_obj = FamilySpendingController()
    return family_spending_obj.family_spending_edit(id)


@app.route('/fx')
def fx():
    return render_template("fxcalc.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
