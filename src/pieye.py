import time
import logging
import numpy as np
from logging import handlers
from picamera2 import Picamera2
from bottle import abort


class PiEye:
    """PiEye

    Main controller class for the Pi-Eye Service
    """

    def __init__(self, debug=False):
        self.logger = self.make_logger(debug)
        self.image_cache = {}

    def make_logger(self, debug):
        """Make Logger

        Args:
            debug (bool): Used to set level of logging - Should be false for normal operation

        Returns:
            logger: python logger instance - used to generate logs.
        """

        # sets logging format
        logFormatter = logging.Formatter(
            "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
        )

        logger = logging.getLogger()

        log_level = logging.DEBUG if debug else logging.INFO
        logger.setLevel(log_level)

        # Make rotating file handler - so log file size is set to a maximum
        fileHandler = handlers.RotatingFileHandler(
            "/home/pi/pieye.log", maxBytes=(1048576 * 5), backupCount=2
        )
        fileHandler.setFormatter(logFormatter)
        logger.addHandler(fileHandler)

        # also log to console
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        logger.addHandler(consoleHandler)

        return logger

    def reinit_camera(self):
        """Reinitialize the Camera
        Attempt to reinitialize the camera controller and reset the configurations


        Returns:
            bool: Returns True if succeeded, False if error encountered
        """
        try:
            # If the camera is already initialized, try to close it first.
            if hasattr(self, "camera"):
                self.camera.close()
                del self.camera

            # Give the camera a minute to think
            time.sleep(2)
            self.logger.debug("Trying to access Camera..")
            self.camera = Picamera2()

            self.logger.debug("Setting up configuration..")
            self.image_config = self.camera.create_still_configuration(
                main={"format": "BGR888"},
                lores={"size": (320, 240), "format": "YUV420"},
                display="lores",
            )

            # ensures sizes match sensor sizes and speeds up capture
            self.camera.align_configuration(self.image_config)
            self.camera.configure(self.image_config)
            self.camera.start()
            self.logger.debug("Done getting camera ready")

            return True
        except Exception as ex:
            self.logger.info("Could not connect to camera" + str(ex))
            abort(
                500,
                "Error when initializing or connecting to the HQ camera module. Probably the cables are slightly out of place. Please reconnect them. Error message: "
                + str(ex),
            )
            return False

    def check_camera_is_setup(self):
        """Check Camera is Setup

        Used to auto-reinitialize camera if something appears to be wrong

        Returns:
            bool: True if camera is setup and working, False if reinitializing didn't work
        """
        self.logger.debug("Checking if already set up camera")
        if hasattr(self, "camera") and self.camera.is_open:
            return True
        else:
            return self.reinit_camera()

    def capture_preview(self):
        """Capture Preview

        Returns:
            array (np.array): preview image
        """
        self.check_camera_is_setup()
        array = self.camera.capture_array("lores")
        self.logger.debug("Took preview photo")
        return array

    def capture_image(self):
        self.check_camera_is_setup()
        now1 = np.datetime64("now")

        array = self.camera.capture_array("main")

        now2 = np.datetime64("now")
        self.logger.debug(now2 - now1, "Took to take image")
        self.logger.debug("Took full resolution image")
        return array

    def capture_image_and_cache(self):
        """Capture Image and Cache
        Captures an image and generates a cache for the image.
        Note that only the latest image is stored in the cache

        Returns:
            array (np.array): Full resolution image
        """
        self.image_cache = {}  # reset cache - only hold one image at a time
        self.check_camera_is_setup()

        now = np.datetime64("now")
        image_name = np.datetime_as_string(now, unit="ms", timezone="UTC")

        array = self.camera.capture_array("main")
        self.image_cache[image_name] = array
        # self.image_cache["latest"] = array  # for easy debugging
        now2 = np.datetime64("now")
        self.logger.debug(now2 - now, "Took to take image")
        self.logger.debug("Took full resolution image")
        return image_name

    def get_cached_image(self, image_name):
        """Get Cached Image
        Returns an image from the cache if found, else None

        Args:
            image_name (str): Name of the image in the cache

        Returns:
            image (np.array or None): Returns the image from the cache as a numpy array, or None if the image could not be found
        """
        return self.image_cache.get(image_name, None)
