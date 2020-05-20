import pandas
import numpy as np

# Still not 100% set on this design - Simon/SmoxBoye.

class DataManager:
    def __init__(self):
        self._dataframes = []
        self._categories = []
    
    def _clean_columns(self, dataframe):
        remove_columns = ["Kvalitet", "Tidsutsnitt"]
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
                        
                        df = self._clean_columns(df)
                        
                        df.insert(0, "time", df["Datum"] + ":" + df["Tid (UTC)"].str[:2])
                        df = df.drop(columns=["Datum", "Tid (UTC)"])
                        #TODO Make categories updatable so if same cat is uploaded the old one gets replaced
                        for cat in [cat for cat in df.columns if cat != "time"]:
                            if cat not in self._categories:
                                single_df = pandas.concat([df["time"], df[cat]], axis=1)
                                self._dataframes.append(single_df)
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
    
    #TODO make get_unit work like a dynamic dict for the category unit
    def get_unit(self, category):
        pass
    
    def get_category(self, category):
        if category not in self._categories:
            return -1
        
        for frame in self._dataframes:
            if category in frame.columns:
                return frame
    
    def get_multiple(self, categories):
        dataframes = []
        
        for cat in categories:
            dataframes.append(self.get_category(cat))
        
        multi = dataframes.pop(0)
        for frame in dataframes:
            multi = multi.merge(frame, how="outer", on="time")
        
        return multi
