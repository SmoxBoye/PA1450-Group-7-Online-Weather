from .datamanager import DataManager
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

class DrawManager():
    def __init__(self):
        pass

    def create_fig(self, df, df_attribute = []):
        fig = px.line(df, x="time", y=df.columns[1])
        return fig

    def create_html(self, dfs, path = "", open = False, units = [], same_y = False, sources = []):
        if units == []:
            units = [""]*len(dfs)
        else:
            for i in range(len(units)):
                units[i] = " (" + units[i] + ")"
        if sources == []:
            sources = [""]*len(dfs)
        else:
            for i in range(len(sources)):
                sources[i] = " (" + sources[i] + ")"

        colors = ["#1f77b4", "#d62728", "#32C77C", "#9467bd", "#ff7f0e", "#1f77b4", "#d62728", "#32C77C", "#9467bd", "#ff7f0e"]
        file_name = []
        fig = go.Figure()

        for i in range(len(dfs)):
            if same_y:
                y_axis = ""
            else:
                y_axis = i + 1
            file_name.append(dfs[i].columns[1])
            fig.add_trace(go.Scatter(
                x = dfs[i].loc[:,dfs[i].columns[0]],
                y = dfs[i].loc[:,dfs[i].columns[1]],
                name=dfs[i].columns[1] + sources[i],
                yaxis="y"+str(y_axis)
            ))

        layout = {}
        if same_y:
            layout["xaxis"]=dict(
                domain=[0, 1]
            )
            layout["yaxis1"]=dict(
                title=dfs[0].columns[1]+units[0],
            )
        else:
            layout["xaxis"]=dict(
                domain=[(len(dfs) - 1) * 0.05, 1]
            )
            layout["yaxis1"]=dict(
                title=dfs[0].columns[1]+units[0],
                titlefont=dict(
                    color="#1f77b4"
                ),
                tickfont=dict(
                    color="#1f77b4"
                ),
                anchor="free",
                side="left",
                position=0
            )
            for i in range(2, 1 + len(dfs)):
                layout["yaxis" + str(i)]=dict(
                    title=dfs[i-1].columns[1]+units[i-1],
                    titlefont=dict(
                        color=colors[i-1]
                    ),
                    tickfont=dict(
                        color=colors[i-1]
                    ),
                    anchor="free",
                    overlaying="y",
                    side="left",
                    position=(i - 1) * 0.05
                )
        fig.update_layout(layout)

        file_name = sorted(file_name)
        file_name = "".join(file_name)
        fig.write_html(path, auto_open=False)
        return path + file_name+".html"


if __name__ == "__main__":

    files = []
    files.append("C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_3_4_65090_20200512_194409.csv")
    files.append("C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_7_65090_20200514_132531.csv")
    files.append("C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_9_65090_20200514_132715.csv")
    files.append("C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_16_65090_20200512_191016.csv")
    files.append("C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_21_65090_20200512_194228.csv")

    dfs = []
    data_m = DataManager()

    for file_number in range(len(files)):
        data_m.load_dataframe(files[file_number])
        #dfs.append(data_m.get_category(data_m.categories[file_number]))
    dfs = data_m.get_multiple(data_m.categories)

    draw_m = DrawManager()
    html_name = draw_m.create_html(dfs, path = "", open = True, units = [data_m.get_unit(category) for category in data_m.categories])
