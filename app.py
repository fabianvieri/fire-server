from flask import Flask, request, Response 
import cv2
import numpy as np
import jsonpickle
import os

app = Flask(__name__)

count = 0

@app.route('/')  
def root(): 
    return '<h1>Hello from server</h1>'

@app.route('/count', methods=["GET"])  
def count():
    global count
    count = count + 1 
    return Response(response=count, status=200)

@app.route('/image', methods=["POST"])  
def image():
    global count 
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response_pickled = jsonpickle.encode(response)
    count = count + 1
    return Response(response=response_pickled, status=200, mimetype="application/json")
  
if __name__ == '__main__': 
    # port = int(os.environ.get('PORT', 5000)) 
    app.run(debug=True) 