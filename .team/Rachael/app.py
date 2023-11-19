# Import Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# # Database Setup
# engine = create_engine("sqlite:///../Resources/attrition.sqlite")

# # Reflect an existing database into a new model
# Base = automap_base()

# # Reflect the tables
# Base.prepare(autoload_with=engine)

# # Save reference to the table
# churn = Base.classes.churn

# Flask Setup
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to the Attrition Forcasting App!"


# Define what to do when a user hits the /about route
@app.route('/about')
def about():
    print("Server received request for 'About' page...")
    return "This app uses machine learning to predict customer attrition."

# Run the Flask App:
if __name__ == "__main__":
   app.run(debug=True)