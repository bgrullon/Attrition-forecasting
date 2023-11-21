# Import Dependencies
from flask import Flask, jsonify
from flask_cors import CORS
from project4data import bar_chart_data


# Flask Setup
app = Flask(__name__)
CORS(app, support_credentials=True)

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    data = bar_chart_data()
    return data


# Run the Flask App:
if __name__ == "__main__":
   app.run(debug=True)