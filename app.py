# Import dependencies.
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
# Import our scraping file.
import scraping

# Set up Flask.
app = Flask(__name__)

# Use PyMongo to set up the MongoDB connection.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create the root route.
@app.route("/")
def index():
    # Find the mars collection in the database.
    mars = mongo.db.mars.find_one()
    # Render a file (template) - rather than raw HTML.
    return render_template("index.html", mars=mars)

# Create the scrape button/route.
@app.route("/scrape")
def scrape():
    # Assign the database to a variable.
    mars = mongo.db.mars
    # Scrape the data using our scraping module - save the return.
    mars_data = scraping.scrape_all()
    # Update our mars database with the scraped data.
    mars.update({}, mars_data, upsert=True)
    # Redirect user to homepage.
    return redirect('/', code=302)

# Tell Flask to run.
if __name__ = "__main__":
    app.run()
