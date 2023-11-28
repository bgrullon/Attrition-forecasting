from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from helpers import Query_Data, generate_fake_data, get_predictions

app = Flask(__name__)
CORS(app, support_credentials=True)

# api for testing
@app.route('/')
def getdata():

    # Call the function to query the Redshift table and wait for response
    results = Query_Data()

    # convert results to JSON
    results = jsonify(results)

    # Return the results as a string
    return results

# api for generating fake data
@app.route('/generate')
def generate():
    
    # Call the function to query the Redshift table and wait for response
    results = generate_fake_data(100)

    # get prediction
    prediction = get_predictions(results)

    # convert results to JSON
    results = jsonify(prediction)

    return results


if __name__ == '__main__':
    app.run(debug=True)
