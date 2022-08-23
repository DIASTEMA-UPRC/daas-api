import os

from flask import Flask

from routes.data_ingesting import data_ingesting
from routes.data_cleaning import data_cleaning
from routes.data_sink import data_sink
from routes.join import join

# Get Flask environment variables
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
FLASK_DEBUG = bool(os.getenv("FLASK_DEBUG", "True"))

# Create Flask app and register blueprints
app = Flask(__name__)
app.register_blueprint(data_ingesting, url_prefix="/data-ingesting")
app.register_blueprint(data_cleaning, url_prefix="/data-cleaning")
app.register_blueprint(data_sink, url_prefix="/data-sink")
app.register_blueprint(join, url_prefix="/join")


# Index route
@app.route("/", methods=["GET"])
def index():
    return "Welcome to the Diastema DaaS API!", 200


# Run Flask app
if __name__ == "__main__":
    app.run(FLASK_HOST, FLASK_PORT, FLASK_DEBUG)
