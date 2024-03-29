
from flask import Flask, render_template
import auth
import consumer
import plant
import db
import alg
import time

app = Flask(__name__)
app.config.from_mapping(
        SECRET_KEY='dev',
    )
db.init_db()
db.get_db()
app.register_blueprint(auth.bp)
app.register_blueprint(plant.bp)
app.register_blueprint(consumer.bp) 

app.run(debug = True)

