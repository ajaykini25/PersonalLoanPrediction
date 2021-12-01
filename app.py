from datetime import datetime

from flask import Flask, render_template, request
import jsonify
import pickle
import numpy as np
import sklearn


# naming our app as app
app = Flask(__name__)

# loading the pickle file for creating the web app
model = pickle.load(open("loan_pred.pk", "rb"))


#defining the different pages of html and specifying the features required to be filled in the html form
@app.route('/')
def index():
    return render_template("index.html")


# @app.route("/sub", methods=["POST"])
# def submit():
#     # HTML -> python file
#     if request.method == "POST":
#         name = request.form["username"]
#     # py -> HTML
#     return render_template("sub.html", n=name)

# creating a function for the prediction model by specifying the parameters and feeding it to the ML model
"""@app.route("/predict", methods=["POST"])
def predict():
    if request.method == 'POST':
        Age = int(request.form['age'])
        Income = int(request.form['income'])
        Family = int(request.form['family'])
        CCAvg = int(request.form['CCAvg'])
        Education = int(request.form['Education'])
        Mortgage = int(request.form['Mortgage'])
        Securities_Account = int(request.form['Securities Account'])
        CD_Account = int(request.form['CD Account'])
        Online = int(request.form['Online'])
        CreditCard = int(request.form['CreditCard'])

    #    int_features = [int(x) for x in request.form.values()]
    #    final_features = [np.array(int_features)]
        prediction = model.predict([[np.array(Age,Income,Family,CCAvg,Education,Mortgage,Securities_Account,CD_Account,Online,CreditCard)]])
        if prediction == 0:
            return render_template('index.html', prediction_texts="No Personal Loan")
        else:
            return render_template('index.html', prediction_text="Personal Loan Offered")
    else:
        return render_template('index.html') """


@app.route("/predict", methods=["POST"])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print("Featues {}".format(final_features))
  #  query = final_features.reshape(1, -1)
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    print("Prediction is %d", prediction)
    if prediction == 0:
        return render_template('sub.html', prediction_texts="No Personal Loan")
    else:
        return render_template('sub.html', prediction_text="Personal Loan Offered")




@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)
