import pandas as pd
import numpy as np
import plotly.express as px

class DrawManager():
    def __init__(self):
        pass

    def create_fig(self,df,df_attribute = []):
        if df_attribute == []:
            df_melt = df.melt(id_vars=["Datum", "Tid (UTC)"], value_vars=df.columns[2]) #supposed the first column is day and second is time, the thrid, or [2], is the first with data in it
            fig = px.line(df_melt, x="Time", y="value")
        else:
            df_melt = df.melt(id_vars=["Datum", "Tid (UTC)"], value_vars=df_attribute)
            fig = px.line(df_melt, x="Time" , y="value")
        return fig

if __name__ == __main__:
    pass
