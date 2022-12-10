
from flask import Flask, render_template

import auth
import home
import consumer
import db

app = Flask(__name__)

db.init_app(app)
app.register_blueprint(auth.bp)
app.register_blueprint(home.bp)
app.register_blueprint(consumer.bp)

app.run(debug = True)