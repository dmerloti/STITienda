from flask import Blueprint, render_template
from database import get_db_connection

tesoro_bp = Blueprint('tesoro', __name__)