import io
import os
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from bottle import route, run, abort, error, yieldroutes, response, static_file



@route("/reinitCamera")
def reinit_camera():
    return {"Initialization":"Successful"}


@route("/getPreview")
def get_preview():
    buf = io.BytesIO()
    array = cv2.imread('fake_server_files/preview.jpg')
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    plt.imsave(buf, array, format="jpeg")
    buf.seek(0)
    byts = buf.read()
    response.set_header('Content-type','image/jpeg')
    return byts





@route("/takeAndCacheImage")
def take_image_and_cache():
    return {'image_name': 'latest'}




@route("/getCachedImage/<image_name>")
def get_cached_image(image_name):
    
    now1 = np.datetime64('now')
    array = cv2.imread('fake_server_files/image.jpg')
    array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
    if array is None:
        abort(590, "Image no longer cached... could not fetch.")
    buf = io.BytesIO()
    plt.imsave(buf, array, format="jpeg")
    buf.seek(0)
    byts = buf.read()
    response.set_header('Content-type','image/jpeg')
    now2 = np.datetime64('now')
    print(now2-now1,'Took to get and buf image')
    
    return byts



@route("/hello")
def hello():
    return "Hello World!"

@route("/")
def list_routes():
    
    return {'valid routes': ["/hello", "/takeAndGetImage", "/getImage", "/takeImage","getPreview","reinitCamera"]}