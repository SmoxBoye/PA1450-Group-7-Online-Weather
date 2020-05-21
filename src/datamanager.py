import pandas
import numpy as np

class DataManager:
    def __init__(self):
        self._dataframes = []
        self._categories = []
        self._cat_unit = {}
    
    def _clean_columns(self, dataframe):
        remove_columns = ["Kvalitet", "Tidsutsnitt"]
        to_be_dropped = [x for x in dataframe.columns for y in remove_columns if x.startswith(y)]

        return dataframe.drop(columns=to_be_dropped).dropna(how="all", axis=1)
    
    def _get_unit_from_file(self,path):
        start = 0
        stop = 0
        stop_search = False
        with open(path) as f:
            for i, row in enumerate(f):
                if row.startswith("Parameternamn;"):
                    start = i
                    stop_search = True
                if row in ["\n", "\r\n"] and stop_search:
                    stop = i - start - 1
                    break
            df = pandas.read_csv(filepath_or_buffer=path, sep=";", skiprows=start, nrows=stop)
            
            for index, row in df.iterrows():
                self._cat_unit[row["Parameternamn"]] = row["Enhet"]
    
    def load_dataframe(self, path):
        """load_dataframe reads path csv file and adds it as a dataframe into self.dataframes.

        Args:
            path (string): the path to the csv file.
        """  

        with open(path) as f:
            for i, row in enumerate(f):
                if row.startswith("Datum;"):
                    df = pandas.read_csv(filepath_or_buffer=path, sep=";", skiprows=i)
                    
                    df = self._clean_columns(df)
                    
                    df.insert(0, "time", df["Datum"] + ":" + df["Tid (UTC)"].str[:2])
                    df = df.drop(columns=["Datum", "Tid (UTC)"])
                    for cat in [cat for cat in df.columns if cat != "time"]:
                        if cat not in self._categories:
                            single_df = pandas.concat([df["time"], df[cat]], axis=1)
                            self._dataframes.append(single_df)
                            self._categories.append(cat)
                        else:
                            single_df = pandas.concat([df["time"], df[cat]], axis=1)
                            for i, frame in enumerate(self._dataframes):
                                if cat in frame.columns:
                                    self._dataframes[i] = single_df
                    break
        self._get_unit_from_file(path)

    
    @property
    def categories(self):
        return self._categories
    
    def get_unit(self, category):
        return self._cat_unit[category]
    
    def get_category(self, category):
        if type(category) is str:
            return self.get_single(category)
        elif type(category) is list and len(category) > 1:
            return self.get_multiple(category)
        else:
            raise TypeError("get_category only supports string or list objects > 1")
    
    def get_single(self, category):
        if category not in self._categories:
            return -1
        
        for frame in self._dataframes:
            if category in frame.columns:
                return frame
    
    def get_multiple(self, categories):
        dataframes = []
        
        for cat in categories:
            dataframes.append(self.get_single(cat))
        
        multi = dataframes.pop(0)
        for frame in dataframes:
            multi = multi.merge(frame, how="outer", on="time")
        
        return multi
