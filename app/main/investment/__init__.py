from flask import Blueprint

investment = Blueprint('investment', __name__, url_prefix='/investments',template_folder='templates')

from . import views
