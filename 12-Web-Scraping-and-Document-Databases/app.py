
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo 
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/app")


@app.route("/")
def index():
    Mars_Facts = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_facts )


@app.route("/scrape")
def scrape():
    
    Mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
