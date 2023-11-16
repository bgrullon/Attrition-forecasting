from flask import Flask, request, jsonify
from flask_cors import CORS
from data import get_counties_list 

app = Flask(__name__)

CORS(app, support_credentials=True)

@app.route('/counties', methods=['POST'])
def get_counties():
    data = request.get_json()
    sqlVar = data.get('data')
    counties = get_counties_list(sqlVar)
    return jsonify(counties)

if __name__ == '__main__':
    app.run(debug=True)