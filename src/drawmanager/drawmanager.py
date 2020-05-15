import pandas as pd
import numpy as np
import plotly.express as px

class DrawManager():
    def __init__(self):
        pass

    def create_fig(self,df,df_attribute = [], time_scope):
        if df_attribute == []:
            fig = px.line(df, x="time", y=df.columns[1])
        else:
            df_melt = df.melt(id_vars="time", value_vars=df_attribute)
            fig = px.line(df_melt, x="time" , y="value")
        return fig

if __name__ == __main__:
    pass
