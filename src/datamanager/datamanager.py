import pandas
import numpy as np

# Still not 100% set on this design - Simon/SmoxBoye.

class DataManager:
    def __init__(self):
        self.dataframes = []
    
    def load_dataframe(self, path):
        """load_dataframe reads path csv file and adds it as a dataframe into self.dataframes.

        Args:
            path (string): the path to the csv file.

        Returns:
            int: error codes; 0: Success, 1: FileNotFoundError, -1: other Errors.
        """  

        # Tries to append path csv as dataframe and send return code.
        try:
            #TODO Skip rows intelligently as the data start at different points in different files.
            self.dataframes.append(pandas.read_csv(filepath_or_buffer="path", sep=";", skiprows=range(9))) 
            return 0
        except FileNotFoundError:
            return 1
        except:
            # If unspecified error occurs will return -1.
            return -1
    
