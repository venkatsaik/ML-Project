from flask import Flask
from flask import request
from flask import jsonify
import datetime

import util
app = Flask(__name__)

# @app.route('/hello/')
# def hello():
#     return util.get_location_names()

@app.route('/get_location_names',methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    location = request.form['location']
    month_ref = request.form['month']
    bedroom = int(request.form['bedroom'])
    x=month_ref.split('-')
    month_num = x[1]
    datetime_object = datetime.datetime.strptime(month_num, "%m")
    month = datetime_object.strftime("%b")
    t_month=(int(x[0])-2000)*12+int(x[1])
    t_month2=t_month**2
    t_month3=t_month**3
    response = jsonify({
        'estimated_price': util.get_estimated_price(location,t_month,bedroom,t_month2,t_month3,month)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For CT Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True ,port=8080,use_reloader=False)