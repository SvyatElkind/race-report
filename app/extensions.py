"""Module for flask extensions instantiation"""
from flasgger import Swagger
from playhouse.flask_utils import FlaskDB
from flask_caching import Cache

from app.static.docs.swagger import template

db_wrapper = FlaskDB()
cache = Cache()
swagger = Swagger(template=template)
