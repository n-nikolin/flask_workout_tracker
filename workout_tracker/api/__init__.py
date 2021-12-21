# Good idea and good practice to have errors in separate file
# and directory. Just have to figure out how and where to implement it

from flask import Blueprint

main = Blueprint('api', __name__)

from . import views