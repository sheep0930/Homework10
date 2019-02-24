from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_db

@app.route("/")
def index():
    listings = db.listings.find_one()
    return render_template("index.html", listings=listings)


@app.route("/scrape")
def scraper():
    listings = db.listings
    listings_data = scrape_mars.scrape()
    listings.update({}, listings_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
