from flask import Flask, request, render_template
from flask import g as Global
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def db_connection():
    client = MongoClient('10.10.252.62', 27017)
    db = client.rent_test_db
    return client, db

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
    client, db = db_connection()
    r_collection = db.rent_collection

    pipeline = [
        {
            '$lookup':
            {
                'from': 'equip_collection',
                'localField': 'equip_id',
                'foreignField': 'equip_id',
                'as': 'equipInfos'
            }
        },
        {'$unwind': '$equipInfos'},
        {
            '$lookup':
            {
                'from': 'user_collection',
                'localField': 'user_id',
                'foreignField': 'user_id',
                'as': 'userInfos'
            }
        },
        {'$unwind': '$userInfos'},
        {
            '$project':
            {
                'id': '$id',
                'state': '$state',
                'equip_id': '$equip_id',
                'equip_name': '$equipInfos.name',
                'user_id': '$user_id',
                'user_email': '$userInfos.email',
                'rent_date': '$rent_date',
                'return_p_date': '$return_p_date',
                'return_date': '$return_date',
                'time_stamp': '$time_stamp',
        }},
        {'$sort': {'time_stamp': 1}},
    ]

    data_dict = {}
    for data in r_collection.aggregate(pipeline):
        data_dict[data['equip_id']] = data

    client.close()

    dblist = list(data_dict.values())
    return render_template('status_table.html', dbdata=dblist)

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