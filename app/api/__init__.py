from flask import Blueprint
from app.api.api_class import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix="/api/v1")

from . import routes