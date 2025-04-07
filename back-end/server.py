from flask import Flask, request, jsonify, render_template, send_from_directory
import util
import os

app = Flask(__name__, static_folder="../client", template_folder="../client")

@app.route("/")
def index():
    return send_from_directory(app.template_folder, "app.html")

@app.route("/get_metadata", methods=["GET"])
def get_metadata():
    regions = util.get_categorical_options().get("region", [])
    response = jsonify({
        "regions": regions
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/predict_expense", methods=["POST"])
def predict_expense():
    age = float(request.form["age"])
    bmi = float(request.form["bmi"])
    children = int(request.form["children"])
    sex = request.form["sex"]
    smoker = request.form["smoker"]
    region = request.form["region"]

    estimated_expense = util.get_estimated_expense(age, bmi, children, sex, smoker, region)

    response = jsonify({
        "estimated_expense": estimated_expense
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server for Insurance Expense Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
