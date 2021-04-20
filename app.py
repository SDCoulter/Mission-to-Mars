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
