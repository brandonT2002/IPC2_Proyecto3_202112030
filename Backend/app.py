from flask import Flask, jsonify, request
from flask_cors import CORS
from Controller import Controller

app = Flask(__name__)
CORS(app)

ctrl = Controller()

@app.route('/')
def ping():
    return jsonify({'message':'API IPC2-Proyecto3'})

@app.route('/profiles',methods=['POST'])
def readProfiles():
    data = request.json
    return ctrl.readProfiles(
        data['filename']
    )

@app.route('/profiles',methods=['GET'])
def getProfiles():
    return ctrl.getProfiles()

@app.route('/messages',methods=['POST'])
def readMessages():
    data = request.json
    return ctrl.readUsers(
        data['filename']
    )

@app.route('/messages',methods=['GET'])
def getMessages():
    return ctrl.getMessages()

@app.route('/getDates',methods=['GET'])
def getDates():
    return ctrl.getDates()

@app.route('/getUsers',methods=['GET'])
def getUsers():
    return ctrl.getUsers()

@app.route('/request1',methods=['POST'])
def request1():
    data = request.json
    return ctrl.service1(
        data['date'],
        data['user'] if data['user'] != 'NONE' else None
    )

@app.route('/request2',methods=['POST'])
def request2():
    data = request.json
    return ctrl.service2(
        data['user'] if data['user'] != 'NONE' else None
    )

@app.route('/request3',methods=['POST'])
def request3():
    data = request.json
    return ctrl.service3(
        data['filename']
    )

@app.route('/reset',methods=['POST'])
def reset():
    data = request.json
    ctrl.initObjects()
    return {'response':'reseted'}

if __name__ == '__main__':
    app.run(debug = True, port = 4000)