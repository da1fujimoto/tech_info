from flask import Flask, request, render_template, redirect
from flask import g as Global
import pymongo
from pymongo import MongoClient
import datetime

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

@app.route('/equip', methods=['POST', 'GET'])
def equip_table():
    if request.method == 'GET':
        client, db = db_connection()
        e_collection = db.equip_collection

        pipeline = [{'$sort': {'time_stamp': 1}}]

        data_dict = {}
        for data in e_collection.aggregate(pipeline):
            data_dict[data['equip_id']] = data

        client.close()

        dblist = list(data_dict.values())
        return render_template('equip_table.html', dbdata=dblist)
    else:
        equip_id = request.form['equip_id']
        name = request.form['name']
        extra = extra=request.form['extra']

        client, db = db_connection()
        e_collection = db.equip_collection

        input_dict = {'equip_id': equip_id, 'name': name, 'extra': extra, 'time_stamp': datetime.datetime.now()}

        e_collection.insert_one(input_dict)
        client.close()

        return redirect('/equip')

@app.route('/equip/<equip_id>')
def equip_edit(equip_id):
    client, db = db_connection()
    e_collection = db.equip_collection

    pipeline = [{'$sort': {'time_stamp': 1}}]

    data_dict = {}
    for data in e_collection.aggregate(pipeline):
        if equip_id == data['equip_id']:
            data_dict[data['equip_id']] = data

    client.close()

    dbdata = data_dict[equip_id]
    return render_template('equip_form.html', dbdata=dbdata)

@app.route('/users', methods=['POST', 'GET'])
def users_table():
    if request.method == 'GET':
        client, db = db_connection()
        u_collection = db.user_collection

        pipeline = [{'$sort': {'time_stamp': 1}}]

        data_dict = {}
        for data in u_collection.aggregate(pipeline):
            data_dict[data['user_id']] = data

        client.close()

        dblist = list(data_dict.values())
        return render_template('users_table.html', dbdata=dblist)
    else:
        user_id = request.form['user_id']
        email = request.form['email']
        extra = extra=request.form['extra']

        client, db = db_connection()
        u_collection = db.user_collection

        input_dict = {'user_id': user_id, 'email': email, 'extra': extra, 'time_stamp': datetime.datetime.now()}

        u_collection.insert_one(input_dict)
        client.close()

        return redirect('/users')

@app.route('/users/<user_id>')
def user_edit(user_id):
    client, db = db_connection()
    u_collection = db.user_collection

    pipeline = [{'$sort': {'time_stamp': 1}}]

    data_dict = {}
    for data in u_collection.aggregate(pipeline):
        if user_id == data['user_id']:
            data_dict[data['user_id']] = data

    client.close()

    dbdata = data_dict[user_id]
    return render_template('users_form.html', dbdata=dbdata)

@app.route('/test')
def test_code():
    return render_template('test.html')

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)