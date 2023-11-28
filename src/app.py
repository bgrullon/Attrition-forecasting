from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from queries import Query_Data

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


if __name__ == '__main__':
    app.run(debug=True)
