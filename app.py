from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import threading
import time

from helpers.yolo_model import load_model
from helpers.media_utils import process_image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "output"

# CREATE FOLDERS IF NOT EXIST
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# LOAD MODEL ONLY ONCE
model, classes = load_model()


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return "No image uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )

    file.save(filepath)

    result = {}

    # START TIMER
    start_time = time.time()

    # THREAD FUNCTION
    def detect():

        plate = process_image(
            filepath,
            model,
            classes,
            OUTPUT_FOLDER
        )

        result["plate"] = plate

    # THREADING
    thread = threading.Thread(target=detect)

    thread.start()

    thread.join()

    # END TIMER
    end_time = time.time()

    response_time = round(
        end_time - start_time,
        2
    )

    plate_text = result.get(
        "plate",
        "No Plate Detected"
    )

    return render_template(
        "index.html",
        plate=plate_text,
        image_path=filepath,
        response_time=response_time
    )


# API ROUTE FOR POSTMAN
@app.route("/api/predict", methods=["POST"])
def api_predict():

    if "image" not in request.files:

        return jsonify({
            "error": "No image uploaded"
        })

    file = request.files["image"]

    if file.filename == "":

        return jsonify({
            "error": "No selected file"
        })

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )

    file.save(filepath)

    result = {}

    # START TIMER
    start_time = time.time()

    def detect():

        plate = process_image(
            filepath,
            model,
            classes,
            OUTPUT_FOLDER
        )

        result["plate"] = plate

    # THREADING
    thread = threading.Thread(target=detect)

    thread.start()

    thread.join()

    # END TIMER
    end_time = time.time()

    response_time = round(
        end_time - start_time,
        2
    )

    return jsonify({
        "plate_number": result.get(
            "plate",
            "No Plate Detected"
        ),
        "response_time": f"{response_time} seconds"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=7860,
        debug=True
    )