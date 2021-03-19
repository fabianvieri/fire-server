from flask import Flask, request, Response 
import cv2
import numpy as np
import jsonpickle
import os

app = Flask(__name__) 

@app.route('/')  
def hello_world(): 
    return '<h1>Hello from server</h1>'

@app.route('/image', methods=["POST"])  
def image(): 
    r = request
    nparr = np.fromstring(r.data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")
  
if __name__ == '__main__': 
    port = int(os.environ.get('PORT')) 
    app.run(port=port) 