import os
from flask import Flask
from flask import render_template



def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # from App import db
    # db.init_app(app)

    from App import auth
    app.register_blueprint(auth.bp)

    return app

# create_app()
