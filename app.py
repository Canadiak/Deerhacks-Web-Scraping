from flask import Flask, request, render_template, url_for, redirect
import sklearn
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", 'rb'))

#replace form.html with whatever the HTML file is called
@app.route('/')
def home():
    return render_template('form.html')

#assuming there's a predict button
@app.route('/predict', methods=['POST'])
def predict():
    team1 = request.form["First Team"]
    year1 = request.form["Year 1"]
    team2 = request.form["Second Team"]
    year2 = request.form["Year 2"]

    #Jeremy will have to do some more data scraping here. To get the team stats based off
    #the name and year provided. There should probably be a check to make sure the team exists
    #in the year provided. I'm assuming he's going to grab them the same way he made the csvs
    #and that the two teams stats are seperate. I'm also going to assume that he's going to create
    #new csvs called team1.csv and team2.csv since Heroku does allow us to create new txt files
    #(the text files get deleted when the application has restarted but that's fine)

    df1 = pd.read_csv('team1.csv', usecols=range(53)).dropna(axis=1)._get_numeric_data()
    df2 = pd.read_csv('team2.csv', usecols=range(53)).dropna(axis=1)._get_numeric_data()
    df  = df1.sub(df2)
    df = df.drop(['Rk', 'G', 'MP', 'FG', '3P', '2P', 'FT', 'TRB', 'PTS', 'Team2', 'L', 'PW', 
    'MOV', 'SOS', 'SRS', 'NRtg', '3PAr', 'Arena', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'TOV%2', 'DRB%', 'FT/FGA2'], axis=1)

    #if there's an error here, it's probably because python is recognizing this as a series and not a dataframe
    #if that problem comes up i know how to fix it
    output = model.predict(df)[0]

    return render_template('form.html', prediction_text=output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)