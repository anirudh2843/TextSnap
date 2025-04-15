from flask import Flask, render_template, request, send_from_directory, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import os

from engine import processor

app = Flask(__name__)
app.config["SECRET_KEY"] = "askjdhfjskd"
app.config["UPLOAD_FOLDER"] = "uploads"

# Make sure uploads directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(ALLOWED_EXTENSIONS, "Only image files are allowed"),
        FileRequired("Please upload an image.")
    ])
    submit = SubmitField("Upload")

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    form = UploadForm()
    result = None
    file_url = None

    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        result = processor(filepath)
        file_url = url_for("get_file", filename=filename)

    return render_template("index.html", form=form, file_url=file_url, result=result)

if __name__ == "__main__":
    app.run(debug=True)
