from flask import Flask
from config import Config
from routes import main
import os

def create_app():
    app = Flask(__name__)

    # app configs
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER

    # make sure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # register blueprints
    app.register_blueprint(main)

    return app

if __name__ == '__main__':
    app = create_app()
    # you can change debug or port here anytime
    app.run(debug=True, host='0.0.0.0', port=5001)



