from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars


app = Flask(__name__)

#mongo = PyMongo(app)
client = pymongo.MongoClient()
db = client.app


@app.route("/")
def index():
    mars_db = db.mars_db.find_one()
#first time when there is no data in the MongoDB    
    if not mars_db:
        mars_db = scrape_mars.scrape()
        db.mars_db.update(
        {},
        mars_db,
        upsert = True
        )
    return render_template("index.html", mars_db = mars_db)

@app.route("/scrape")
#scrape the data
def scrape():
    mars_data = scrape_mars.scrape()
    db.mars_db.update(
    {},
    mars_data,
    upsert = True
    )

    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug = True)
