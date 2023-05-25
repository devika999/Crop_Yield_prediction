from flask import Flask, render_template, request
# import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
@app.route('/',methods=['GET'])
def Home():
    return render_template('home.html')

@app.route('/rt',methods=['GET'])
def rt():
    return render_template('rain_temp.html')
@app.route('/index',methods=['GET'])
def index():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Item = request.form['Item']
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        avg_temp = request.form['avg_temp']
        area = request.form['area']
        y_pred = [[Item, Year, average_rain_fall_mm_per_year, avg_temp]]
        if(Item=='Maize'):
                Item = 1
        elif(Item=='Potatoes'):
                Item = 3
        elif(Item=='Rice'):
                Item = 4
        elif(Item=='Sorghum'):
            Item = 5
        elif(Item=='Soybeans'):
            Item = 6
        elif(Item=='Wheat'):
            Item = 8
        elif(Item=='Cassava'):
            Item = 0
        elif(Item=='Sweet potatoes'):
            Item = 7    
        elif(Item=='Yams'):
            Item = 10
        else:
            Item = 2
            
        
        prediction=(pickle.load(open('random_forest_regression_model.pkl', 'rb'))).predict([[Item,Year, average_rain_fall_mm_per_year, avg_temp]])
        output=prediction*4
        area = area
        if output<0:
            return render_template('index.html',prediction_text="Sorry invalid data")
        else:
            return render_template('index.html',prediction_text="Maximum yield {} in Kg".format(output))
    else:
        return render_template('index.html')

@app.route("/rtpredict", methods=['POST'])
def rtpredict():
    if request.method == 'POST':
        Country = request.form['Country']
        Year = request.form['Year']
        y_pred = [[Country, Year]]
        if(Country=='Argentina'):
                Country = 3
        elif(Country=='Brazil'):
                Country = 13
        elif(Country=='Canada'):
                Country = 18
        elif(Country=='India'):
            Country = 40
        elif(Country=='Pakistan'):
            Country = 71
        else:
            Country = 84
            
        
        prediction1=(pickle.load(open('rf_model_rainfall.pkl', 'rb'))).predict([[Country,Year]])
        prediction2=(pickle.load(open('rf_model_temp.pkl', 'rb'))).predict([[Country,Year]])
        output1=prediction1
        output2=prediction2
        if output1<0:
            return render_template('rain_temp.html',prediction_text="Sorry invalid data")
        else:
            return render_template('rain_temp.html',prediction_text1="Average rainfall per year: {}".format(output1),prediction_text2="Average temperature per year: {}".format(output2))
    else:
        return render_template('rain_temp.html')

@ app.route('/crop_recommend')
def crop_recommend():
    title = 'Crop Recommendation'
    return render_template('crop_recommend.html', title=title)

@ app.route('/crop_recom', methods=['POST'])
def crop_recom():
    title = 'Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['nitrogen'])
        P = int(request.form['phosphorous'])
        K = int(request.form['pottasium'])
        temperature=int(request.form['temperature'])
        humidity=int(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        my_prediction=(pickle.load(open('RFcrop_recommendation.pkl', 'rb'))).predict([[N, P, K, temperature, humidity, ph, rainfall]])

        return render_template('crop_recommend.html', prediction=my_prediction, title=title)

      
if __name__=="__main__":
    app.run(host='0.0.0.0')
