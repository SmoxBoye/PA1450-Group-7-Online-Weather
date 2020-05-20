"""Core Flask app routes."""
from flask import render_template
from flask import current_app as app
from flask import request, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from .drawmanager import DrawManager
from .datamanager import DataManager


ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def home():
    dm = DrawManager()
    df = DataManager()
    """Landing page."""
    if request.method == 'POST':
        # check if the post request has the file part
        print("DAB")
        if 'file' in request.files:
            print("2")
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                print("3")
                file.save("data/data.csv")
                print(df.load_dataframe("data/data.csv"))
                print(len(df.categories))
                category = df.categories[0]
                dataf = df.get_category(category)
                print(dataf)
                fig = dm.create_fig(dataf)
                fig.write_html('application/templates/' + str(category) + '.html', auto_open=False)


    return render_template(
        'index.html',
    )


@app.route("/graph", methods=["GET"])
def show_graph():
    return render_template("first_figure.html")
