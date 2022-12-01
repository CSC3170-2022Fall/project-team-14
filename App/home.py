from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from auth import login_required

bp = Blueprint('home', __name__)

@bp.route('/index_consumer')
def index():
    return render_template('index_consumer.html')