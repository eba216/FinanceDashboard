from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

import yfinance as yf

def validate_ticker(form, field):
    stock = field.data.upper()
    ticker = yf.Ticker(stock)
    
    if not ticker.info['regularMarketPrice']:
        raise ValidationError(f"Cannot obtain info on {stock}, it does not exist. \nCheck again for correct ticker.")

class StockForm(FlaskForm):
    stock_name = StringField("", default = "TSLA", validators=[DataRequired(), validate_ticker],
    render_kw = {"align":"center", "onchange": "this.form.submit()"})