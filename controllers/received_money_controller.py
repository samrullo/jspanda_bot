import datetime
from models.received_money import ReceivedMoney
import logging
from flask import flash
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class ReceivedMoneyForm(FlaskForm):
    date = StringField("date", render_kw={"class": "form-control"})
    amount_usd = StringField("amount_usd", render_kw={"class": "form-control"})
    exchange_rate = StringField("exchange_rate", render_kw={"class": "form-control"})
    submit = SubmitField("Save received money", render_kw={"class": "btn btn-lg btn-dark"})


class ReceivedMoneyController:
    def __init__(self):
        self.model = ReceivedMoney()

    def show_all_received_money(self):
        received_money_records = self.model.get_items()
        return render_template("received_money_main.html", received_money_records=received_money_records)

    def received_money_add(self):
        form = ReceivedMoneyForm()
        logging.info(f"form hidden tag : {form.hidden_tag()}")
        if form.validate_on_submit():
            date = datetime.datetime.strptime(form.date.data, '%Y%m%d')
            amount_usd = int(form.amount_usd.data)
            exchange_rate = float(form.exchange_rate.data)
            self.model.add_item(date, amount_usd, exchange_rate)
            flash(f"Saved {date} {amount_usd} {exchange_rate} successfully", "success")
            return self.show_all_received_money()
        return render_template("received_money_add.html", form=form)

    def received_money_remove(self, id):
        self.model.remove_item(id)
        record = self.model.get_item(id)
        if not record:
            flash(f"Successfully removed {id} record", "success")
        else:
            flash(f"Couldn't remove {id}", "failure")
        return self.show_all_received_money()
