
from flask import Flask, render_template

import auth

app = Flask(__name__)
app.register_blueprint(auth.bp)

if __name__ == '__main__':
    app.run(debug = True)