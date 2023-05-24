
from flask import Flask, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
import requests
import os
import re


API_URL = "https://api-inference.huggingface.co/models/SanketJadhav/PlantDiseaseClassifier-Resnet50"
headers = {"Authorization": "Bearer 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"}

app = Flask(__name__)

upload_folder = os.path.join("static", "uploads")
app.config['UPLOADED_PATH'] = upload_folder

def remove_underscore(name):
    return re.sub(r'_+', ' ', name)

def classify(filename):
    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)

    labels = list(map(lambda x: (round(x['score'], 5), remove_underscore(x['label'])), response.json()))

    return labels

@app.route('/', methods=['GET', 'POST'])
def home():

    # else just render the basic template 
    return render_template("homepage.html")

@app.route('/trial', methods=['GET', 'POST'])
def trial():
    # saves the image in directory
    if request.method == 'POST':
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOADED_PATH'], filename))

            img_path = os.path.join(app.config['UPLOADED_PATH'], filename)

            labels = classify(img_path)

            return render_template("trialpage.html", img_path=img_path, labels=labels)

    return render_template("trialpage.html")

@app.route('/response', methods=['GET', 'POST'])
def response():
    if request.method == 'POST':
        file = request.files.get('img_path')
        print(file)
        return render_template("response.html", name="I like anime", img_path=img_path, labels=labels)

    # else just render the basic template 
    return render_template("response.html")

@app.context_processor
def utility_processor():
    def classify(filename):
        with open(filename, "rb") as f:
            data = f.read()

        response = requests.post(API_URL, headers=headers, data=data)

        labels = map(lambda x: {round(x['score'], 4), remove_underscore(x['label'])}, response.json())

        return labels

    return dict(classify=classify)

if __name__ == "__main__":
    app.run(debug=True)
