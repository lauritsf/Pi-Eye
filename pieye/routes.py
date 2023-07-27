import io
import os
import datetime
import socket
from bottle import route, abort, response
from tempfile import TemporaryDirectory

try:
    from picamera2 import Picamera2  # pylint: disable=import-error
except ImportError:
    from pieye.camera import Picamera2


def init_camera():
    """
    Initliaze the camera and set its configuration.
    This involves creating preview and still configurations,
    and starting the camera.
    
    Returns:
        Picamera2: Initialized camera instance"""
    camera = Picamera2()

    # Define preview and still configurations for the camera
    camera.preview_configuration = camera.create_preview_configuration(
        main={"size": (320, 240), "format": "RGB888"}
    )
    camera.still_configuration = camera.create_still_configuration(raw={})
    camera.configure("preview")

    camera.start()
    return camera

# Initialize the global camera instance
camera = init_camera()


@route("/camera/reinitialize")
def reinit_camera():
    """
    Reinitialize the camera. This is useful if the there's a problem with the current camera instance.
    This route closes the current camera instance and reinitializes it.
    
    Returns:
        dict: JSON response indicaing success of the operation.
    """
    global camera
    camera.close()
    camera = init_camera()

    response_data = {
        "status": "success",
        "message": "Camera reinitialized successfully",
    }

    response.status = 200
    response.content_type = "application/json"
    return response_data


@route("/camera/preview")
def get_preview():
    """Fetch a preview image from the camera.

    Returns:
        bytes: A JPEG image buffer.

    Raises:
        500: An error occurred fetching the preview image.
    """
    try:
        image = camera.capture_image("main")

        # Convert image array to bytes buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="jpeg")
        image_buffer.seek(0)

        response.set_header("Content-type", "image/jpeg")
        return image_buffer.getvalue()
    except Exception as e:
        abort(500, "Error when getting preview image: " + str(e))


@route("/camera/still-capture")
def get_still():
    """
    Captures a still image and saves it as a dng file. The image is then returned as a bytes buffer.

    Returns:
        bytes: A DNG image data.

    Raises:
        500: An error occurred capturing the image.
    """
    try:
        # Construct filename from system timestamp and hostname
        hostname = socket.gethostname()
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{hostname}_{formatted_time}.dng"

        # Create temporary directory and file path
        tempdir = TemporaryDirectory()
        filepath = os.path.join(tempdir.name, filename)

        # Capture still image and save as DNG
        camera.switch_mode_and_capture_file("still", filepath, name="raw")

        # Read DNG image data from file
        with open(filepath, "rb") as f:
            dng_image_data = f.read()

        response.content_type = "application/x-adobe-dng"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"

        return dng_image_data
    except Exception as e:
        abort(500, "Error when capturing still image: " + str(e))


@route("/")
def list_routes():
    """
    Lists the valid routes for the PiEye Server. Acts as the landing page for the server.

    Returns:
        dict: Dictionary of valid routes
    """
    return {"valid routes": [
        "/",
        "/camera/reinitialize",
        "/camera/preview",
        "/camera/still-capture",
    ]}

