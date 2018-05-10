from flask import Flask, request, render_template, redirect, Response
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
        return str(request)

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
        eid = data['equip_id']
        data_dict[eid] = data
        data_dict[eid]['time_stamp'] += datetime.timedelta(hours=9)
        if data_dict[eid]['rent_date'] != None:
            data_dict[eid]['rent_date'] += datetime.timedelta(hours=9)
            data_dict[eid]['rent_date'] = str(data_dict[eid]['rent_date']).split()[0]
        if data_dict[eid]['return_p_date'] != None:
            if datetime.datetime.now() > data_dict[eid]['return_p_date']:
                data_dict[eid]['over'] = 1
            else:
                data_dict[eid]['over'] = 0
            data_dict[eid]['return_p_date'] += datetime.timedelta(hours=9)
            data_dict[eid]['return_p_date'] = str(data_dict[eid]['return_p_date']).split()[0]
        if data_dict[eid]['return_date'] != None:
            data_dict[eid]['return_date'] += datetime.timedelta(hours=9)
            data_dict[eid]['return_date'] = str(data_dict[eid]['return_date']).split()[0]

    client.close()

    dblist = list(data_dict.values())
    return render_template('status_table.html', dbdata=dblist)

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
    else: # POST
        equip_id = request.form['equip_id']
        name = request.form['name']
        extra = extra=request.form['extra']

        client, db = db_connection()
        e_collection = db.equip_collection

        input_dict = {'equip_id': int(equip_id), 'name': name, 'extra': extra, 'time_stamp': datetime.datetime.now()}

        e_collection.insert_one(input_dict)
        client.close()

        return redirect('/equip')

@app.route('/equip/<int:equip_id>')
def equip_edit(equip_id):
    client, db = db_connection()
    e_collection = db.equip_collection
    dbdata = e_collection.find_one({'equip_id': equip_id}, sort=[('time_stamp', -1)])
    client.close()

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
    else: # POST
        user_id = request.form['user_id']
        email = request.form['email']
        extra = extra=request.form['extra']

        client, db = db_connection()
        u_collection = db.user_collection

        input_dict = {'user_id': int(user_id), 'email': email, 'extra': extra, 'time_stamp': datetime.datetime.now()}

        u_collection.insert_one(input_dict)
        client.close()

        return redirect('/users')

@app.route('/users/<int:user_id>')
def user_edit(user_id):
    client, db = db_connection()
    u_collection = db.user_collection
    dbdata = u_collection.find_one({'user_id': user_id}, sort=[('time_stamp', -1)])
    client.close()

    return render_template('users_form.html', dbdata=dbdata)

@app.route('/admin')
def admin_code():
    client, db = db_connection()
    r_collection = db.rent_collection
    u_collection = db.user_collection
    e_collection = db.equip_collection
    pipeline = [
        {'$sort': {'time_stamp': -1}},
    ]

    r_data = r_collection.aggregate(pipeline)
    u_data = u_collection.aggregate(pipeline)
    e_data = e_collection.aggregate(pipeline)
    client.close()

    r_dblist = []
    for data in r_data:
        r_dblist.append(data)
        r_dblist[-1]['time_stamp'] += datetime.timedelta(hours=9)
        if r_dblist[-1]['rent_date'] != None:
            r_dblist[-1]['rent_date'] += datetime.timedelta(hours=9)
        if r_dblist[-1]['return_p_date'] != None:
            r_dblist[-1]['return_p_date'] += datetime.timedelta(hours=9)
        if r_dblist[-1]['return_date'] != None:
            r_dblist[-1]['return_date'] += datetime.timedelta(hours=9)

    u_dblist = []
    for data in u_data:
        u_dblist.append(data)
        u_dblist[-1]['time_stamp'] += datetime.timedelta(hours=9)

    e_dblist = []
    for data in e_data:
        e_dblist.append(data)
        e_dblist[-1]['time_stamp'] += datetime.timedelta(hours=9)

    return render_template('admin.html', r_dbdata=r_dblist, u_dbdata=u_dblist, e_dbdata=e_dblist)

@app.route('/update', methods=['POST', 'GET'])
def update_seq():
    if request.method == 'GET':
        return redirect('/status')
    else: # POST
        client, db = db_connection()
        r_collection = db.rent_collection
        u_collection = db.user_collection
        e_collection = db.equip_collection

        if 'equip_name' not in request.form.keys() or 'user_email' not in request.form.keys():
            print('not set name error')
            return redirect('/status')

        equip_name = request.form['equip_name']
        user_email = request.form['user_email']

        if 'equip_id' not in request.form.keys():
            equipdata = e_collection.find_one({'name': request.form['equip_name']}, sort=[('time_stamp', -1)])
            if equpdata != None:
                equip_id = equipdata['equip_id']
            else:
                equipdata = e_collection.find_one(sort=[('equip_id', -1)])
                equip_id = equipdata['equip_id'] + 1
                input_dict = {'equip_id': int(equip_id), 'name': equip_name, 'extra': '', 'time_stamp': datetime.datetime.now()}
                e_collection.insert_one(input_dict)
        else:
            equip_id = request.form['equip_id']

        if 'user_id' not in request.form.keys():
            userdata = u_collection.find_one({'email': request.form['user_email']}, sort=[('time_stamp', -1)])
            if userdata != None:
                user_id = userdata['user_id']
            else:
                userdata = e_collection.find_one(sort=[('user_id', -1)])
                user_id = userdata['user_id'] + 1
                input_dict = {'user_id': int(user_id), 'email': user_email, 'extra': '', 'time_stamp': datetime.datetime.now()}
                u_collection.insert_one(input_dict)
        else:
            user_id = request.form['user_id']

        if 'action' in request.form.keys() and request.form['action'] == '返却':
            input_dict = {
                'state': 0,
                'equip_id': int(equip_id),
                'user_id': int(user_id),
                'rent_date': None,
                'return_p_date': None,
                'return_date': datetime.datetime.now(),
                'time_stamp': datetime.datetime.now()
            }
        else:
            input_dict = {
                'state': 1,
                'equip_id': int(equip_id),
                'user_id': int(user_id),
                'rent_date': datetime.datetime.now(),
                'return_p_date': datetime.datetime.now() + datetime.timedelta(days=7),
                'return_date': None,
                'time_stamp': datetime.datetime.now()
            }
        r_collection.insert_one(input_dict)

        client.close()

        return redirect('/status')

@app.route('/postest', methods=['POST', 'GET'])
def postest():
    print(request.method)
    return redirect('/')

@app.route('/toPostURL', methods=['POST'])
def get_user_info():
    username =  request.form['username'];
    age = request.form['age'];
    print(username, age, request.method)
    response = Response()
    response.status_code = 200
    return response