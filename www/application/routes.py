"""Core Flask app routes."""
from flask import render_template, send_file, send_from_directory
from flask import current_app as app
from flask import request
from .drawmanager import DrawManager
from .datamanager import DataManager
import os


ALLOWED_EXTENSIONS = {'csv', 'xml'}
smhi_to_yr = {"Lufttemperatur" : "temperature", "Byvind" : "windSpeed", "Lufttryck reducerat havsytans nivå" : "pressure", "Vindriktning" : "windDirection", "Nederbördsmängd" : "precipitation", "" : ""}
draw = DrawManager()
data = DataManager()
data.load_dataframe("data/data.xml")
data.load_dataframe("data/downloads/Moln.csv")
data.load_dataframe("data/downloads/Regn.csv")
data.load_dataframe("data/downloads/Temperatur.csv")
data.load_dataframe("data/downloads/Tryck.csv")
data.load_dataframe("data/downloads/Vindhastighet.csv")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_key(val):
    for key, value in smhi_to_yr.items():
         if val == value:
             return key


@app.route('/', methods=["GET", "POST"])
def home():
    """Landing page."""

    return render_template(
        'index.html',
    )


@app.route('/live', methods=["GET", "POST"])
def live():
    return render_template(
        'live.html',
    )


@app.route("/export/<string:category>", methods=["POST", "GET"])
def export(category):
    #start = int(st.replace("-", ""))
    #end = int(ed.replace("-", ""))
    file = open("export.csv", "w")
    file.write(data.export(category))
    file.close()
    # print(category)
    # print(start)
    # print(end)
    return send_file("export.csv", attachment_filename=f"export.csv", as_attachment=True)


@app.route("/categories/<string:dir_name>/<string:cat_name>", methods=["GET"])
def send_cat(cat_name, dir_name):
    #print(send_from_directory("application/templates/categories", cat_name + ".html"))
    print(cat_name)
    return render_template("categories/" + dir_name + "/" + cat_name + ".html")


@app.route("/upload/<string:extension>", methods=["POST"])
def upload(extension):
    if request.method == 'POST':
        print("1")
        if 'file' in request.files:
            print("2")
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                category = ""
                dfs = []
                print("3")
                file.save("data/data" + "." + extension)
                print(data.load_dataframe("data/data" + "." + extension))
                print(len(data.categories))
                for i in range(0, len(data.categories)):
                    category = str(data.categories[i])
                    if category in smhi_to_yr.keys():
                        dfs = []
                        category = data.categories[i]
                        df = data.get_category(category)
                        dfs.append(df)
                        dfs.append(data.get_category(smhi_to_yr[str(category)]))
                        draw.create_html(dfs, 'application/templates/categories/uploaded/' + str(category) + '.html')
    return render_template(
        'index.html',
    )
