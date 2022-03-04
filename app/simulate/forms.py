from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError

from ..main.forms import validate_ticker


def validate_stock_simulation_range(form, field):
    if field.data < 0:
        raise ValidationError("Number must be greater than 0")
    if field.data > 100:
        raise ValidationError("Number must be less that 100")

        
class StockSimulatorForm(FlaskForm):
    num_sims = IntegerField(default=10, label="Number of Simulations (max 100)",
                            validators=[DataRequired(), validate_stock_simulation_range])
    stock_name = StringField("Stock Ticker", validators=[DataRequired(), validate_ticker])
    sim_time = SelectField("Simulation Years",default=(1,1), choices=[(1, 1), (3, 3), (5, 5), (10, 10)], coerce=int)