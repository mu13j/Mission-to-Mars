# import necessary libraries
from flask import Flask, render_template
import pymongo
import scrape_mars


# create instance of Flask app
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.scrape

@app.route("/scrape")
def scrape():
    data = scrape_mars.scrape()
    db.collection.insert_one(data)
    return "Scraped some data"

# create route that renders index.html template
@app.route("/")
def home():
    forecasts = list(db.collection.find())
    print(forecasts)
    return render_template("index.html", forecasts=forecasts, tables=forecasts[0]['facts'])


if __name__ == "__main__":
    app.run(debug=True)