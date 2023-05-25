import io
from flask import Flask, render_template, Response
import cv2
import socket
import io
import numpy as np

import numpy as np
import cv2

#~~~~~~~~~FLASK STUFF~~~~~~~~~~~~#
app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming ."""
    return render_template('./index.html')
def gen():
    """Video streaming generator function."""
    vc = cv2.VideoCapture(0)
    err_arr =cv2.imread("error.jpg")
    error_img = cv2.imencode('.jpg', err_arr)[1].tobytes()
    vc.set(cv2.CAP_PROP_FPS, 10)
    
    while True:
        rval, cur_frame = vc.read()
        if rval:            
            stream_img = cv2.imencode('.jpg', cur_frame)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream_img + b'\r\n')
        else:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + error_img + b'\r\n')



@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000,debug=True, threaded=True)
