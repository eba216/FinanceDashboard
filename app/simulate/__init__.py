from flask import Blueprint

simulate = Blueprint("simulate", __name__)

from . import views