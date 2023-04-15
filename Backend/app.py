from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def ping():
    return jsonify({'message':'API IPC2-Proyecto2'})

if __name__ == '__main__':
    app.run(debug = True, port = 4000)