from flask import Flask
from routes import api_images


app = Flask(__name__)


app.register_blueprint(api_images)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
