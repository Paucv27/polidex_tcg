from flask import Flask, render_template, request, jsonify
import numpy as np
from flask_cors import CORS
from recognition import process_card
from scraping import fetchListings

app = Flask(__name__)
CORS(app)

@app.route("/process-image", methods=["POST"])
def process_image():

    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    name, number = process_card(file)

    result = fetchListings(name, number)

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)