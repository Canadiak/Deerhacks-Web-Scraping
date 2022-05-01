from flask import Flask, request, render_template, url_for, redirect
import sklearn
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", 'rb'))

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    Weight         = int(request.form["Weight"])
    Age            = int(request.form["Age"])
    Height         = int(request.form["Height"])

    final_features = [np.array([Weight, Age, Height])]
    prediction     = model.predict(final_features)
    output         = prediction[0]

    return render_template('form.html', prediction_text=output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)