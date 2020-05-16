"""Core Flask app routes."""
from flask import render_template
from flask import current_app as app
from flask import request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os


@app.route('/', methods=["GET", "POST"])
def home():
    """Landing page."""
    if request.method == 'POST':
        # check if the post request has the file part
        print("DAB")
        if 'file' in request.files:
            print("2")
            file = request.files['file']
            if file.filename != '':
                print("3")
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template(
        'index.html',
        title='Weather Application',
        description='Very nice',
        template='home-template',
        body="yeet"
    )
