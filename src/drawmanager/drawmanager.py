from datamanager import DataManager
import pandas as pd
import numpy as np
import plotly.express as px

class DrawManager():
    def __init__(self):
        pass

    def create_fig(self, df, df_attribute = []):
        if df_attribute == []:
            fig = px.line(df, x="time", y=df.columns[1])
        else:
            df_melt = df.melt(id_vars="time", value_vars=df_attribute)
            fig = px.line(df_melt, x="time" , y="value")
        return fig

if __name__ == "__main__":
    data_m = DataManager()
    file = "C:/Users/tobia/OneDrive/Documents/GitHub/PA1450-Group-7-Online-Weather/downloads/smhi-opendata_3_4_65090_20200512_194409.csv"
    data_m.load_dataframe(file)
    df = data_m.get_category(data_m.categories[0])
    draw_m = DrawManager()
    fig = draw_m.create_fig(df)
    fig.write_html('first_figure.html', auto_open=True)
