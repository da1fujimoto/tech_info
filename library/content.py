from flask import Flask, request, render_template
from flask import g as Global
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def db_connection():
    client = MongoClient('10.10.252.62', 27017)
    db = client.rent_test_db
    collection = db.rent_test_collection
    return client, collection

# @app.before_request
# def before_request():
#     Global.mongo_collection = db_connection()

@app.route('/', methods=['POST', 'GET'])
def app_route():
    if request.method == 'GET':
        return render_template('sample_template.html')
    elif request.method == 'POST':
        print(request.method)
        print(request)
        return 'ok'

@app.route('/status')
def app_status():
    client, collection = db_connection()
    dbd = collection.find({})
    client.close()
    return render_template('status_table.html', dbdata=list(dbd))

@app.route('/about')
def app_about():
    return render_template('base.html')

@app.route('/camera')
def qr_code():
    return render_template('qr_code.html')

@app.route('/test')
def test_code():
    return render_template('test.html')

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)