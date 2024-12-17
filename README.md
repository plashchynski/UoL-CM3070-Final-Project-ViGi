# ViGi: A camera surveillance system

This is a final project for University of London [BSc Computer Science programme](https://www.london.ac.uk/study/courses/undergraduate/bsc-computer-science).
Consult [Report.pdf](/Report.pdf) for more information.

## Features

* Multiple camera support
* Motion detection
* Object recognition
* Web server to view the camera feed and recordings
* Notifications via SMS and email

## Requirements

- Python 3.8 or higher. Tested with Python 3.12
- OpenCV
- A USB camera that can be accessed via OpenCV

## Installation and usage

```bash
pip install vigi
vigi
```

## Configuration

A detailed configuration options are available in the [Configuration](docs/configuration.md) document.

The agent can be configured in two ways:
* Using the `vigi.ini` file. This method is recommended for production use and when configuration is
constant and does not change frequently.
* Using command line arguments. This method is recommended for development and testing purposes:

```txt
usage: vigi [-h] [--debug] [--no-monitor] [--data-dir DATA_DIR] [--camera-id CAMERA_ID] [--host HOST] [--port PORT] [--max-errors MAX_ERRORS]
               [--sensitivity SENSITIVITY] [--detection-model-file DETECTION_MODEL_FILE] [--disable-detection] [--inference-device INFERENCE_DEVICE]
               [--http-basic-username HTTP_BASIC_USERNAME] [--http-basic-password HTTP_BASIC_PASSWORD] [--http-basic-hash HTTP_BASIC_HASH]

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable debug mode
  --no-monitor          Disable the camera monitor
  --data-dir DATA_DIR   Directory to store the recordings
  --camera-id CAMERA_ID
                        Camera ID to monitor
  --host HOST           Host to run the web server
  --port PORT           Port to run the web server
  --max-errors MAX_ERRORS
                        Maximum number of consecutive errors when reading a frame from the camera
  --sensitivity SENSITIVITY
                        Sensitivity of the motion detector, should be a float between 0 and 1
  --detection-model-file DETECTION_MODEL_FILE
                        Path to the detection model file (YOLO's yolov8n.pt, by default)
  --disable-detection   Disable object detection
  --inference-device INFERENCE_DEVICE
                        Inference device for object detection (cpu or cuda)
  --http-basic-username HTTP_BASIC_USERNAME
                        Username for HTTP basic authentication. Disabled by default
  --http-basic-password HTTP_BASIC_PASSWORD
                        Password for HTTP basic authentication
  --http-basic-hash HTTP_BASIC_HASH
                        Hashed password for HTTP basic authentication
```

You can configure additional cameras by adding a [CAMERAn] section to the `vigi.ini` file, where n is the camera ID. The only required parameter is the `CameraID`:

```ini
[CAMERA0]
CameraID = 0

[CAMERA1]
CameraID = 1

MaxErrors=50
Sensitivity=0.5

```

You can specify `MaxErrors` and `Sensitivity` for each camera separately. If these parameters are not specified, the default values will be used.


## Installation on Raspberry Pi (Raspberry Pi OS)

64 bit OS is required for PyTorch to work. Tested with [Raspberry Pi OS (Legacy, 64-bit)](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-legacy-64-bit).

Install the pip package:
```bash
pip install vigi
```

Run the agent:
```bash
./.local/bin/vigi --host 0.0.0.0
```

If the object detection is slow on your device, you can try to run the agent with the `--disable-detection` option to disable it.

# Notifications

Consult the [Notifications](docs/notifications.md) document for more information on how to configure notifications.

# Development

## Run from the sources

```bash
# Set up a virtual environment
python -m venv .venv
. .venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# run the agent
python main.py
```

## Build a pip package

```bash
pip install build
python -m build
```

## Publish the package to PyPI

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
```

## Run unit tests

Download a samples dataset for the motion detection tests from [here](https://vigi-statics.s3.us-west-2.amazonaws.com/samples.zip) and extract it to the `tests/` directory.

Then run the tests:

```bash
python -m unittest discover
```

## Test coverage

To generate a coverage report, run the following command:

```bash
pip install coverage
coverage run -m unittest discover
coverage html
```

## Run PyLint

```bash
pylint $(git ls-files '*.py')
```
