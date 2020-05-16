import pandas
import numpy as np

# Still not 100% set on this design - Simon/SmoxBoye.

class DataManager:
    def __init__(self):
        self._dataframes = []
        self._categories = []
    
    def _clean_columns(self, dataframe):
        remove_columns = ["Kvalitet", "Tidsutsnitt", "Vindriktning"]
        to_be_dropped = [x for x in dataframe.columns for y in remove_columns if x.startswith(y)]
        #print(dataframe.columns)
        #print(to_be_dropped)
        return dataframe.drop(columns=to_be_dropped).dropna(how="all", axis=1)
    
    def load_dataframe(self, path):
        """load_dataframe reads path csv file and adds it as a dataframe into self.dataframes.

        Args:
            path (string): the path to the csv file.

        Returns:
            int: error codes; 0: Success, 1: FileNotFoundError, -1: other Errors.
        """  

        # Tries to append path csv as dataframe and send return code.
        try:
            with open(path) as f:
                for i, row in enumerate(f):
                    if row.startswith("Datum;"):
                        df = pandas.read_csv(filepath_or_buffer=path, sep=";", skiprows=i)
                        #print(df)
                        df = self._clean_columns(df)
                        #print(df)
                        df.insert(0, "time", df["Datum"] + ":" + df["Tid (UTC)"].str[:2])
                        df = df.drop(columns=["Datum", "Tid (UTC)"])
                        self._dataframes.append(df)
                        for cat in [cat for cat in df.columns if cat != "time"]:
                            if cat not in self._categories:
                                self._categories.append(cat)
                        break
            return 0
        except FileNotFoundError:
            return 1
        except Exception as e:
            print(f"\nError: {e} \n")
            # If unspecified error occurs will return -1.
            return -1
    
    @property
    def categories(self):
        return self._categories
    
    def get_category(self, category):
        if category not in self._categories:
            return -1
        
        for frame in self._dataframes:
            if category in frame.columns:
                return frame
