# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 16:56:36 2020

@author: MariangelGarcia
# Taked from here https://developer.ibm.com/technologies/artificial-intelligence/tutorials/deploy-a-python-machine-learning-model-as-a-web-service/
# adpated for a model with multiple features
"""

import pickle
import flask
import os
#import lightgbm as lgb

app = flask.Flask(__name__)
port = int(os.getenv("PORT", 9099))

#Import the model file that was created previously:
model = pickle.load(open("clf.pkl","rb"))

# Add a route that 
#will allow you to send a JSON body of features and will return a prediction:
@app.route('/predict', methods=['POST'])
def predict():
    #take the features from the jason
    features = flask.request.get_json(force=True)['features']
    #Build the prediction
    prediction = model.predict([features],num_iteration=model.best_iteration)[0]
    #Return 1 or 0
    prediction = prediction.round(0)
    response = {'prediction': prediction}
    return flask.jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
    



