"""Core Flask app routes."""
from flask import render_template
from flask import current_app as app
from flask import request, redirect, flash, url_for, send_from_directory
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
    draw = DrawManager()
    data = DataManager()
    """Landing page."""
    if request.method == 'POST':
        # check if the post request has the file part
        print("1")
        if 'file' in request.files:
            print("2")
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                print("3")
                file.save("data/data.csv")
                print(data.load_dataframe("data/data.csv"))
                print(len(data.categories))
                category = data.categories[0]
                df = data.get_category(category)
                #print(df)
                fig = draw.create_fig(df)
                fig.write_html('application/templates/categories/uploaded/' + str(category) + '.html', auto_open=False)
                file.save("data/uploaded/" + str(category) + ".css")

    return render_template(
        'index.html',
    )


@app.route('/live', methods=["GET", "POST"])
def live():
    return render_template(
        'live.html',
    )


@app.route("/export/<string:start>/<string:end>", methods=["POST", "GET"])
def export(st, ed):
    start = int(st.replace("-", ""))
    end = int(ed.replace("-", ""))
    return render_template(
        'index.html',
    )


@app.route("/categories/<string:dir_name>/<string:cat_name>", methods=["GET"])
def send_cat(cat_name, dir_name):
    #print(send_from_directory("application/templates/categories", cat_name + ".html"))
    print(cat_name)
    return render_template("categories/" + dir_name + "/" + cat_name + ".html")


