import io
import os
import cv2
import base64
import numpy as np
import matplotlib.pyplot as plt
from pieye import PiEye
from bottle import route, run, abort, error, yieldroutes, response, static_file


# Initialized the Pi-Eye controller class instance
eye = PiEye(debug=False)


@route("/reinitCamera")
def reinit_camera():
    """Route for reinitializing the camera - In case something goes wrong.
    See PiEye.reinit_camera for more details
    """
    result = eye.reinit_camera()
    return {"Camera Reinitialized": str(result)}


@route("/getPreview")
def get_preview():
    """Get PiEye Preview Image

    Returns:
        byts: bytes image buffer with preview image
    """ ""
    buf = io.BytesIO()
    array = eye.capture_preview()

    # convert to RGB
    array = cv2.cvtColor(array, cv2.COLOR_YUV420p2BGR)

    # save array to buffer - faster than saving the image to disk
    plt.imsave(buf, array, format="jpeg")

    buf.seek(0)
    byts = buf.read()
    response.set_header(
        "Content-type", "image/jpeg"
    )  # for debugging, displays as a jpeg in the browser
    return byts


@route("/takeAndCacheImage")
def take_and_cache_image():
    """Take and Cache an Image

    This takes a single full resolution image and stores it in memory.
    It gives a response telling the user the name of that image, so they know
    it was taken successfully and gives a unique identifier so they can retrieve
    that exact same image later
    """
    now1 = np.datetime64("now")
    image_name = eye.capture_image_and_cache()

    now2 = np.datetime64("now")
    eye.logger.debug(now2 - now1, "Took to get and cache image")
    return {"image_name": image_name}


@route("/getCachedImage/<image_name>")
def get_cached_image(image_name):
    """Get Cached Image

    Args:
        image_name (str): name of the image to be retrieved from the cache (note: only the latest image can be retrieved)

    Returns:
        byts: a bytes buffer of the full image if found.
    """
    now1 = np.datetime64("now")

    array = eye.get_cached_image(image_name)

    if array is None:
        abort(590, "Image no longer cached... could not fetch.")
    buf = io.BytesIO()
    plt.imsave(buf, array, format="jpeg")
    buf.seek(0)
    byts = buf.read()
    response.set_header("Content-type", "image/jpeg")

    now2 = np.datetime64("now")
    eye.logger.debug(now2 - now1, "Took to get and buf image")

    return byts


@route("/")
def list_routes():
    """List Routes

    Landing page for the server. Lists the valid routes.
    """
    return {
        "valid routes": [
            "/reinitCamera",
            "/getPreview",
            "/takeAndCacheImage",
            "/getCachedImage/[image-name]",
        ]
    }
