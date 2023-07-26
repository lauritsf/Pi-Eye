from PIL import Image
import numpy as np
import logging

_log = logging.getLogger(__name__)


class Picamera2:
    """Mock Picamera2 Class

    This class is a mock of the Picamera2 class from the picamera2 package.
    It provides a subset of the functionality of the Picamera2 class, and is
    intended to be used for testing and development when a Raspberry Pi is not
    available.
    """

    def __init__(self):
        """Initialize the camera."""
        self.runing = False
        self.started = False

        try:
            self._open_camera()
        except Exception:
            _log.error("Camera __init__ sequence did not complete.")
            raise RuntimeError("Camera __init__ sequence did not complete.")

    def _open_camera(self):
        if not self._initialize_camera():
            raise RuntimeError("Failed to initialize camera")

        self.is_open = True
        _log.info("Camera is now open.")

    def _initialize_camera(self):
        # Harcode to match HQ camera
        self.sensor_resolution = (4056, 3040)
        self.sensor_format = "SBGGR12_CSI2P"

        _log.info("Initialization successful.")
        return True

    def close(self):
        if not self.is_open:
            return

        self.is_open = False
        self.camera_config = None
        self.preview_configuration = None
        self.still_configuration = None
        self.video_configuration = None
        _log.info("Camera closed successfully.")

    def create_preview_configuration(
        self,
        main={},
        lores=None,
        raw={},
        transform=None,
        colour_space=None,
        buffer_count=4,
        controls={},
        display="main",
        encode="main",
        queue=True,
    ) -> dict:
        if (
            lores != None
            or raw != {}
            or transform != None
            or colour_space != None
            or buffer_count != 4
            or controls != {}
            or display != "main"
            or encode != "main"
            or queue != True
        ):
            raise NotImplementedError("Only main preview implemented for fake camera")

        default_main = {"format": "XBGR8888", "size": (640, 480)}
        for key, value in main.items():
            default_main[key] = value

        config = {
            "use_case": "preview",
            "main": main,
            "lores": None,
            "raw": None,
            "display": "main",
            "encode": "main",
        }
        return config

    def create_still_configuration(
        self,
        main=None,
        lores=None,
        raw=None,
        transform=None,
        colour_space=None,
        buffer_count=1,
        controls={},
        display=None,
        encode=None,
        queue=True,
    ) -> dict:
        if main is not None:
            main.setdefault("format", "BGR888")
            main.setdefault("size", (4056, 3040))

        if raw is not None:
            raw.setdefault("format", "SBGGR12_CSI2P")
            raw.setdefault("size", (4056, 3040))

        config = {
            "use_case": "still",
            "main": main,
            "lores": lores,
            "raw": raw,
            "display": display,
            "encode": encode,
        }
        return config

    def configure(self, camera_config="preview"):
        self.configure_(camera_config=camera_config)

    def configure_(self, camera_config="preview"):
        if self.started:
            raise RuntimeError("Camera must be stopped before configuring")

        initial_config = camera_config
        if isinstance(camera_config, str):
            if camera_config == "preview":
                camera_config = self.preview_configuration
            elif camera_config == "still":
                camera_config = self.still_configuration
            else:
                raise ValueError(
                    "Only preview and still use cases implemented for fake camera"
                )
        elif isinstance(camera_config, dict):
            camera_config = camera_config.copy()
        else:
            raise TypeError("camera_config must be a string or dict")
        if camera_config is None:
            camera_config = self.create_preview_configuration()

        # Mark as unconfigured
        self.camera_config = None

        # Skip checking the config etc

        # Mark as configured
        self.camera_config = camera_config

        if initial_config == "preview":
            self.preview_configuration.update(camera_config)
        elif initial_config == "still":
            self.still_configuration.update(camera_config)
        else:
            raise ValueError(
                "Only preview and still use cases implemented for fake camera"
            )

    def start_(self):
        if self.camera_config is None:
            raise RuntimeError("Camera has not been configured")
        if self.started:
            return

        self.started = True

    def start(self, config=None, show_preview=False):
        """Start the camera system running."""
        if show_preview:
            NotImplementedError("Preview not implemented for fake camera")

        if self.camera_config is None and config is None:
            config = "preview"
        if config is not None:
            self.configure(config)
        if self.camera_config is None:
            raise RuntimeError("Camera has not been configured")
        self.start_()

    def capture_image(
        self, name: str = "main", wait=None, signal_function=None
    ) -> Image.Image:
        if wait is not None or signal_function is not None:
            raise NotImplementedError(
                "wait and signal_function not implemented for fake camera"
            )

        if name not in ["main", "raw"]:
            raise NotImplementedError(
                f"Only main and raw images implemented for fake camera, not {name}"
            )

        use_case = self.camera_config["use_case"]
        if use_case == "preview":
            image = Image.open("fake_camera_files/preview.jpg")
        elif use_case == "still":
            image = Image.open("fake_camera_files/image.jpg")
        else:
            raise NotImplementedError(
                "Only preview and still use cases implemented for fake camera"
            )

        return image

    def capture_array(self, name="main", wait=None, signal_function=None):
        image = self.capture_image(name, wait, signal_function)
        array = np.array(image)
        return array

    def stop(self):
        if not self.started:
            _log.debug("Camera was not started.")
            return

        self.started = False
        _log.info("Camera stopped")

    def switch_mode_and_capture_buffers(
        self, camera_config, names=["main"], wait=None, signal_function=None
    ):
        if wait is not None or signal_function is not None:
            raise NotImplementedError(
                "wait and signal_function not implemented for fake camera"
            )

        self.stop()
        self.configure(camera_config)

        buffers = []
        for name in names:
            array = self.capture_array(name)
            buffers.append(array.flatten())

        metadata = {
            "SensorTimestamp": 12962000558000,
            "ExposureTime": 66657,
            "ColourTemperature": 4563,
            "FocusFoM": 585,
            "Lux": 6.656125545501709,
            "AnalogueGain": 8.0,
            "FrameDuration": 66991,
            "SensorTemperature": 0.0,
            "ColourCorrectionMatrix": (
                1.977162480354309,
                -0.8602268695831299,
                -0.11694049835205078,
                -0.36278989911079407,
                1.8365914821624756,
                -0.47379639744758606,
                -0.08924030512571335,
                -0.5866686701774597,
                1.6759089231491089,
            ),
            "AeLocked": True,
            "SensorBlackLevels": (4096, 4096, 4096, 4096),
            "ColourGains": (2.763126850128174, 1.5419270992279053),
            "DigitalGain": 1.0001275539398193,
            "ScalerCrop": (2, 0, 4052, 3040),
        }

        return buffers, metadata

    def switch_mode_and_capture_file(self, camera_config, filepath, name):
        # make a copy of the "fake_camera_files/full.dng" file
        with open("fake_camera_files/full.dng", "rb") as f:
            dng_image_data = f.read()

        # ignore metadata
        # ignore dng_buffer

        # save as dng to tmp folder
        with open(filepath, "wb") as f:
            f.write(dng_image_data)

    class helpers:
        @staticmethod
        def save_dng(dng_buffer, metadata, config, filepath):
            # make a copy of the "fake_camera_files/full.dng" file
            with open("fake_camera_files/full.dng", "rb") as f:
                dng_image_data = f.read()

            # ignore metadata
            # ignore dng_buffer

            # save as dng to tmp folder
            with open(filepath, "wb") as f:
                f.write(dng_image_data)
