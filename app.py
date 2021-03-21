from flask import Flask, request, Response, jsonify, render_template
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
    try:
        data = json.loads(request.json)
        image = data["image"]
        status = data["status"]
        
        conn = db_connect()
        cursor = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query_update = "UPDATE image SET created_date = '%s', image_str = '%s', status = %d WHERE id = 1" % (date, image, status)
        cursor.execute(query_update)
        conn.commit()
    except:
        conn.rollback()
        resp = {'message':'error updating database'}
        return Response(response=json.dumps(resp), status=400, mimetype="application/json")
    finally:
        conn.close()
        
    resp = {'message':'image received'}
    return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/get/image', methods=["GET"])  
def get_image():
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, image_str, created_date FROM image WHERE id = 1")
        row = cursor.fetchall()
    except:
        print("error selecting database")
    finally:
        conn.close()
        response = jsonify({'status':row[0][0], 'image':row[0][1], 'date':row[0][2]})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/show/image')  
def show(): 
    return render_template('show.html')

if __name__ == '__main__': 
    app.run(debug=True, threaded=True) 