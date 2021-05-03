# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api

# Create an instance of Flask
from analytics.realtime import RealTime
from analytics.core import Visits
from analytics.core import Home
from analytics.core import Daily
from analytics.core import Acquire
from analytics.custom import Custom

app = Flask(__name__)
app.secret_key = "a random string"
# Create the API
api = Api(app)


# Use in-memory storage
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return "Hi!", 200


# Uses v3
api.add_resource(RealTime, "/realtime")
api.add_resource(Visits, "/device-visits")
api.add_resource(Home, "/home")
api.add_resource(Daily, "/daily")
api.add_resource(Acquire, "/acquire")
api.add_resource(Custom, "/custom")
