from os import stat
from flask import Flask, request, jsonify, render_template
from datetime import datetime
import sqlite3
import json

app = Flask(__name__)

def db_connect():
    conn = None
    try:
        conn = sqlite3.connect('sfh.sqlite')
    except:
        print("There was problem in database")
    return conn

@app.route('/')  
def root(): 
    return render_template('index.html')
      
@app.route('/post/image', methods=["POST"])  
def post_image():
    response = {}
    status_code = 200
    try:
        # for python request
        data = json.loads(request.json)
        image = data["image"]
        status = data["status"]
        user = data["user"]
        camera = data["camera"]
        date = data["date"]

        conn = db_connect()
        cursor = conn.cursor()
        query_update = "UPDATE camera SET date = '%s', base64_image = '%s', status = %d WHERE user_id = %d AND id = %d" % (date, image, status, user, camera)
        cursor.execute(query_update)            
        conn.commit()
        
        response = {'message':'image received'}
    except:
        conn.rollback()
        response = {'message':'error updating image'}
        status_code = 400
    finally:
        conn.close()           
        
    return jsonify(response), status_code

@app.route('/get/image', methods=["GET"])  
def get_image():
    user = request.args.get('id')
    camera = request.args.get('camera')
    response = {}
    status_code = 200
    if user and camera:
        try:
            conn = db_connect()
            cursor = conn.cursor()
            query_select = "SELECT date, base64_image, status FROM camera WHERE user_id = %s AND id = %s" % (user, camera)
            cursor.execute(query_select)
            row = cursor.fetchall()
            if len(row) == 0:
                response = {'message':'image not found'}
                status_code = 400
            else:
                response = {'date':row[0][0], 'image':row[0][1], 'status':row[0][2]}
        except:
            response = {'message':'error getting image'}
            status_code = 400
        finally:
            conn.close()
    else:
        response = {'message':'invalid parameter'}
        status_code = 400

    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code

@app.route('/post/notification', methods=["POST"])  
def post_notification():
    response = {}
    status_code = 200
    try:
        data = json.loads(json.dumps(request.json))
        image = data["image"]
        status = data["status"]
        user = data["user"]
        date = data["date"]

        conn = db_connect()
        cursor = conn.cursor()
        query_insert = "INSERT INTO notification (date, status, user_id, base64_image) VALUES ('%s', '%s', %d, '%s')" % (date, status, user, image)
        cursor.execute(query_insert)
        conn.commit()
        
        response = {'message':'notification received'}
    except:
        conn.rollback()
        response = {'message':'error push notification'}
        status_code = 400
    finally:
        conn.close()

    return jsonify(response), status_code

@app.route('/get/notification', methods=["GET"])  
def get_notification():
    user = request.args.get('id')
    response = {}
    status_code = 200
    if user:
        try:
            conn = db_connect()
            cursor = conn.cursor()
            query_select = "SELECT n.id, n.date, n.status, n.base64_image, u.name, u.phone, u.address FROM notification n JOIN user u ON n.user_id = u.id WHERE user_id = %s" % (user)
            cursor.execute(query_select)
            row = cursor.fetchall()
            if len(row) == 0:
                response = {'message':'notification not found for this user'}
                status_code = 400
            else:
                notificationList = []
                for record in row:
                    data = {
                        'notificationId':record[0], 
                        'date':record[1],
                        'status':record[2], 
                        'image':record[3], 
                        'name':record[4],
                        'phone':record[5], 
                        'address':record[6]
                    }
                    notificationList.append(data)
                response = notificationList
        except:
            response = {'message':'error getting notification'}
            status_code = 400
        finally:
            conn.close()
    else:
        response = {'message':'invalid parameter'}
        status_code = 400

    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code

@app.route('/done/notification', methods=["POST"])  
def done_notification():
    response = {}
    status_code = 200
    try:
        data = json.loads(json.dumps(request.json))
        notif_id = data["notificationId"]

        conn = db_connect()
        cursor = conn.cursor()
        query_update = "UPDATE notification SET status = 'done' WHERE id = %d" % (notif_id)
        cursor.execute(query_update)            
        conn.commit()
        response = {'message':'notification updated to done'}
    except:
        conn.rollback()
        response = {'message':'error updating notification'}
        status_code = 400
    finally:
        conn.close()           
        
    return jsonify(response), status_code

@app.route('/get/firefighter', methods=["GET"])
def get_firefighter():
    firefighter = request.args.get('id')
    response = {}
    status_code = 200
    if firefighter:
        try:
            conn = db_connect()
            cursor = conn.cursor()
            query_select = "SELECT name, phone, address FROM firefighter WHERE id = %s" % (firefighter)
            cursor.execute(query_select)
            row = cursor.fetchall()
            if len(row) == 0:
                response = {'message':'fire fighter not found'}
                status_code = 400
            else:
                response = {'name':row[0][0], 'phone':row[0][1], 'address':row[0][2]}
        except:
            response = {'message':'error getting fire fighter'}
            status_code = 400
        finally:
            conn.close()
    else:
        response = {'message':'invalid parameter'}
        status_code = 400
    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code

@app.route('/delete/notification', methods=["GET"]) 
def delete_notification():
    user = request.args.get('id')
    response = {}
    status_code = 200
    if user:
        try:
            conn = db_connect()
            cursor = conn.cursor()
            query_select = "DELETE FROM notification WHERE user_id = %s" % (user)
            cursor.execute(query_select)
            row = cursor.fetchall()
            response = {'message':'notification for user_id = %s has been deleted' % (user)}
        except:
            response = {'message':'error delete notification'}
            status_code = 400
        finally:
            conn.close()
    else:
        response = {'message':'invalid parameter'}
        status_code = 400

    response = jsonify(response)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response, status_code
    
@app.route('/show/image')  
def show(): 
    return render_template('show.html')

if __name__ == '__main__': 
    app.run(debug=True, threaded=True) 