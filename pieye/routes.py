import io
import os
import datetime
import socket
from bottle import route, abort, response, template
from tempfile import TemporaryDirectory

# picamera2 is installed by default on the Raspberry Pi OS image.
# For development, the mock camera is used instead.
try:
    from picamera2 import Picamera2  # pylint: disable=import-error
except ImportError:
    from pieye.camera import Picamera2


def init_camera():
    """Initialize the camera and set its configuration.
    
    Returns:
        Picamera2: Initialized camera instance"""
    camera = Picamera2()

    camera.preview_configuration = camera.create_preview_configuration(
        main={"size": (320, 240), "format": "RGB888"}
    )
    camera.still_configuration = camera.create_still_configuration(
        main={"size": (4056, 3040), "format": "RGB888"},
        raw={}
        )
    camera.configure("preview")
    camera.start()

    return camera

# Initialize the global camera instance
camera = init_camera()


@route("/reinitialize")
def reinit_camera():
    """Reinitialize the camera if there's an issue with the current instance.

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


@route("/quick-preview")
def get_quick_preview():
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

@route("/full-preview")
def get_full_preview():
    """Fetch a full resolution preview image from the camera.

    Returns:
        bytes: A JPEG image buffer.

    Raises:
        500: An error occurred fetching the preview image.
    """
    try:
        image = camera.switch_mode_and_capture_image("still", name="main")

        # Convert image array to bytes buffer
        image_buffer = io.BytesIO()
        image.save(image_buffer, format="jpeg")
        image_buffer.seek(0)

        response.set_header("Content-type", "image/jpeg")
        return image_buffer.getvalue()
    except Exception as e:
        abort(500, "Error when getting full resolution preview image: " + str(e))

@route("/capture")
def capture_still():
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


from bottle import request, template, json_dumps

@route("/")
def list_routes():
    """
    Lists the valid routes for the PiEye Server. Acts as the landing page for the server.
    """
    routes = [
        {"url": "/reinitialize", "description": "Reinitialize Camera", "method": "GET"},
        {"url": "/quick-preview", "description": "Quick Preview", "method": "GET"},
        {"url": "/full-preview", "description": "Full Resolution Preview", "method": "GET"},
        {"url": "/capture", "description": "Capture Image", "method": "GET"},
    ]

    # Check query parameter first
    format = request.query.get('format', 'html').lower()

    # If no query parameter provided, then check the Accept header
    if 'application/json' in request.headers.get('Accept', '') and format != 'html':
        response.content_type = "application/json"
        return json_dumps({"routes": routes})

    # Default to HTML format
    html_response = """
        <h2>Available Routes:</h2>
        <pre><code>
        % for route in routes:
            <a href="{{route['url']}}">{{route['url']}}</a> - {{route['description']}} ({{route['method']}})
        % end
        </code></pre>
    """
    
    response.content_type = "text/html"
    return template(html_response, routes=routes)