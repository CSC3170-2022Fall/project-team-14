
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

while (True):
    if(alg.time_queue.empty() == False):
        cur_time = int((time.time() - alg.global_start_time)*100)
        next_exe = alg.time_queue.get()
        while (next_exe[0] <= cur_time and alg.time_queue.empty() == False):
            alg.handle(next_exe)
            next_exe = alg.time_queue.get()
        if(next_exe[0] > cur_time):
            alg.time_queue.put(next_exe)