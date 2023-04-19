import flask
from flask import Flask
from flask_restful import Api, Resource, request
import numpy as np
import pandas as pd
from flask_cors import CORS
import time
from agora_token_builder import RtcTokenBuilder
# for env var 
import os


# from sklearn.tree import DecisionTreeClassifier
# from sklearn import tree
# from sklearn.preprocessing import KBinsDiscretizer 

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r'*': {'origins':'*'}})
api = Api(app)


class testApi(Resource):
     def get(self, name):
         return {"v3, name is: ": name}

class testApi2(Resource):
     def post(self, food):
         return {"v3, favoret food is: ": food}

@app.route('/json_example', methods=['POST', 'GET'])
def handle_json():
    data = request.get_json()
    d = {
         'dayOfWeek': data["dayOfWeek"], 
         'durationArr': data["durationArr"], 
         'day': data["day"]
         }
    df = pd.DataFrame(data=d)
    df = df.astype(float)


    temp = df.groupby(["day"],as_index=False).sum()
    temp = temp[["day", "durationArr"]]


    df = df[["day", "dayOfWeek"]]
    df = df.join(temp.set_index('day'), on='day', how='right')
    df = df.drop_duplicates()

    
    df = df.groupby(["dayOfWeek"]).mean()
        # for testing 
    # print("printing: \n", flush=True)
    # print(df, flush=True)
    resp = flask.Response(df.durationArr.tolist())
    resp.headers['Access-Control-Allow-Origin'] = 'https://productivitypangolin.com' #str(os.getenv('CORS_ORIGINS'))
    return df.durationArr.tolist()

class forToken(Resource):
     def get(self, channel):
        # env vars for agora
        appID = str(os.getenv('agroaAppID') )
        appCertificate = str( os.getenv('agoraAppCertificate') )
        channelName = str(channel)
        uid = 0 # idk where to get the acutual number 
        role = 0 # idk what this even should be 
        expireTimeInSeconds = 3600

        currentTimestamp = int(time.time())
        privilegeExpiredTs = currentTimestamp + expireTimeInSeconds
        token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, role, privilegeExpiredTs)
        
        return {"token: ": token}

api.add_resource(forToken, "/get_token/<string:channel>")


# desision tree 
# @app.route('/DecisionTree', methods=['POST', 'GET'])
# def handle_json_for_tree():
#     data = request.get_json()
#     # set up dataframe 
#     d = {'day': data["day"], 
#          'durationArr': data["durationArr"], 
#          'time': data['time'],
#          }
    
#     df = pd.DataFrame(data=d)
#         # not sure you want the whole thing to be float 
#     df = df.astype(float)


#     y = { 'focusAndWork': data['focusAndWork']}
#     y = pd.DataFrame(data=y)
#     print(y,flush=True)
#         # bin y 
#     enc = KBinsDiscretizer(n_bins=5)
#     y = enc.fit_transform(y)
#     print(y,flush=True)
    
#     #need radome seed? 
#     decision_tree = DecisionTreeClassifier(random_state=0, max_depth=5)
#     decision_tree = decision_tree.fit(df,y.toarray())
#     text_representation = tree.export_text(decision_tree)
#     print("code ran", flush=True)
#     print(text_representation, flush=True)

#     # print("printing: \n", flush=True)
#     # print(df, flush=True)
#     return {"hi" : True}

api.add_resource(testApi, "/test/<string:name>")
api.add_resource(testApi2, "/test2/<string:data>")

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=80)
    # app.run()