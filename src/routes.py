import io
import os
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from pieye import PiEye
from bottle import route, run, abort, error, yieldroutes, response, static_file



eye = PiEye(debug=True)

@route("/reinitCamera")
def reinit_camera():
    eye.reinit_camera()
    return {"Initialization":"Successful"}


@route("/getPreview")
def get_preview():
    buf = io.BytesIO()
    array = eye.capture_preview()
    array = cv2.cvtColor(array, cv2.COLOR_YUV420sp2RGB)
    plt.imsave(buf, array, format="jpeg")
    buf.seek(0)
    byts = buf.read()
    response.set_header('Content-type','image/jpeg')
    return byts


@route("/takeImageAndSave")
def take_image_and_save():
    array = eye.capture_image()
    now = np.datetime64('now')
    fn = np.datetime_as_string(now, unit='ms', timezone='UTC') + '_photo.png'
    fp = os.path.join('/tmp', fn)
    #array = cv2.cvtColor(array, cv2.COLOR_RGBA2RGB)
    
    now1 = np.datetime64('now')
    cv2.imwrite(fp, array)
    
    now2 = np.datetime64('now')
    print(now2-now1,'Took to write image to tmp :(')
    return {'fn': fn}



@route("/takeAndCacheImage")
def take_image_and_cache():
    now1 = np.datetime64('now')
    image_name = eye.capture_image_and_cache()
    
    now2 = np.datetime64('now')
    print(now2-now1,'Took to get and cache image')
    return {'image_name': image_name}



@route("/getImage/<filename>")
def get_image(filename):
    fp = os.path.join('/tmp',filename)
    #buf = io.BytesIO()
    #array = cv2.imread(fp)
    #plt.imsave(buf, array, format="jpeg")
    #buf.seek(0)
    #byts = buf.read()
    #response.set_header('Content-type','image/jpeg')
    return static_file(filename, root='/tmp')



@route("/getCachedImage/<image_name>")
def get_cached_image(image_name):
    
    now1 = np.datetime64('now')
    array = eye.get_cached_image(image_name)
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


@route("/takeAndGetImage")
def take_and_get_image():
    now1 = np.datetime64('now')
    buf = io.BytesIO()
    array = eye.capture_image()
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