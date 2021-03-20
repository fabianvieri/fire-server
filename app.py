from flask import Flask, request, Response, jsonify
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

try:
    conn = db_connect()
    cursor = conn.cursor()
    query = """CREATE TABLE image (
        id integer NOT NULL,
        created_date datetime NOT NULL,
        image_str text,
        status integer NOT NULL
    )"""
    cursor.execute(query)
    conn.commit()
    query = "INSERT INTO image VALUES (1, '2021-03-20 19:41:00', '', 0)"
    cursor.execute(query)
    conn.commit()
except:
    conn.rollback()
    print("table image already exists")

@app.route('/')  
def root(): 
    return '<h1>SFH Server</h1>'
      
@app.route('/post/image', methods=["POST"])  
def post_image():
    data = json.loads(request.json)
    image = data["image"]
    status = data["status"]

    try:
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
    # convert back string
    # bytes = image.encode()
    # base = base64.b64decode(bytes)
    # nparr = np.fromstring(base, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    # cv2.imwrite("frame.jpg", img)
    resp = {'message':'image received'}
    return Response(response=json.dumps(resp), status=200, mimetype="application/json")

@app.route('/get/image', methods=["GET"])  
def get_image():
    try:
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT status, image_str FROM image WHERE id = 1")
        row = cursor.fetchall()
    except:
        print("error selecting database")
    finally:
        conn.close()
        return jsonify({'status':row[0][0], 'image':row[0][1]})

if __name__ == '__main__': 
    app.run(debug=True, threaded=True) 