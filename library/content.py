from flask import Flask, render_template
from flask import g as Global
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def db_connection():
    client = MongoClient('127.0.0.1', 27017)
    db = client.iris_db
    collection = db.iris_collection
    return collection

@app.before_request
def before_request():
    print('mongo_connection')
    Global.mongo_collection = db_connection()

@app.route('/')
def app_route():
    return render_template('sample_template.html')

@app.route('/status')
def app_status():

    dbd = Global.mongo_collection.find()
    return render_template('base.html', dbdata=list(dbd))

@app.route('/about')
def app_about():
    return render_template('base.html')