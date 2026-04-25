from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
from werkzeug.utils import secure_filename
from predictor import LungCancerPredictor
from dotenv import load_dotenv
from PIL import Image
import numpy as np

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "secret-key")

# ---------------- CONFIG ----------------
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

predictor = LungCancerPredictor()

# ---------------- DEMO USERS ----------------
USERS_DB = {
    "rakshith": {
        "password": "Rakshith@21",
        "full_name": "Dr. Rakshith"
    }
}

# ---------------- HELPER FUNCTIONS ----------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def is_ct_scan(image_path):
    """
    Reject colorful images (basketball, selfies)
    Allow grayscale images (CT scans)
    """
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        arr = np.array(img)

        r = arr[:, :, 0]
        g = arr[:, :, 1]
        b = arr[:, :, 2]

        diff_rg = np.mean(np.abs(r - g))
        diff_gb = np.mean(np.abs(g - b))
        diff_rb = np.mean(np.abs(r - b))

        # If colors are very different → not CT
        if diff_rg > 20 or diff_gb > 20 or diff_rb > 20:
            return False

        return True

    except:
        return False


# ---------------- ROUTES ----------------

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/register")
def register_page():
    return render_template("register.html")


@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")

    # Accept ANY username/password
    session["logged_in"] = True
    session["username"] = username

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/home")
def home():

    if not session.get("logged_in"):
        return redirect(url_for("index"))

    return render_template("home.html", username=session.get("username"))


@app.route("/prediction")
def prediction():

    if not session.get("logged_in"):
        return redirect(url_for("index"))

    return render_template("prediction.html")


@app.route("/dashboard")
def dashboard():

    if not session.get("logged_in"):
        return redirect(url_for("index"))

    return render_template("dashboard.html")


@app.route("/performance")
def performance():

    if not session.get("logged_in"):
        return redirect(url_for("index"))

    metrics = predictor.get_model_performance()

    return render_template("performance.html", metrics=metrics)


# ---------------- PREDICTION ----------------

@app.route("/predict", methods=["POST"])
def predict():

    if not session.get("logged_in"):
        return jsonify({"error": "Not authenticated"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        file.save(filepath)

        # Validate CT-like image
        if not is_ct_scan(filepath):

            os.remove(filepath)

            return jsonify({
                "error": "Invalid image. Please upload a lung CT scan image."
            }), 400

        try:

            result = predictor.predict(filepath)

            os.remove(filepath)

            return jsonify(result)

        except Exception as e:

            if os.path.exists(filepath):
                os.remove(filepath)

            return jsonify({
                "error": f"Prediction failed: {str(e)}"
            }), 500

    return jsonify({
        "error": "Invalid file type. Please upload PNG, JPG or JPEG."
    }), 400


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    app.run(debug=True, host="0.0.0.0", port=5000)