import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'static/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define color range (Example: Blue)
LOWER_BOUND = np.array([100, 150, 50])  # Adjust for other colors
UPPER_BOUND = np.array([140, 255, 255])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Process image
            image = cv2.imread(filepath)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, LOWER_BOUND, UPPER_BOUND)
            result = cv2.bitwise_and(image, image, mask=mask)

            output_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.png")
            cv2.imwrite(output_path, result)

            return render_template("index.html", filename="output.png")

    return render_template("index.html", filename=None)

@app.route('/static/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
