from flask import Blueprint, blueprints
from sqlalchemy import exc
from werkzeug.exceptions import BadRequest

bp = Blueprint('error', __name__)

@bp.errorhandler(400)
def bad_request(error):
    pass

@bp.errorhandler(500)
def data_error(error):
    pass
