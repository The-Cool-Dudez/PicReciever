from flask import Blueprint

bp = Blueprint('receiver', __name__)

import app.receiver.routes
