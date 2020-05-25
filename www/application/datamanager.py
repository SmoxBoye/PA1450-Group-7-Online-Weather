import pandas
import numpy as np
import xml.etree.ElementTree as et
import io
import json


class DataManager:
    def __init__(self):
        self._dataframes = []
        self._categories = []
        self._cat_unit = {}

    def _clean_columns(self, dataframe):
        remove_columns = ["Kvalitet", "Tidsutsnitt"]
        to_be_dropped = [x for x in dataframe.columns for y in remove_columns if x.startswith(y)]

        return dataframe.drop(columns=to_be_dropped).dropna(how="all", axis=1)

    def _get_unit_from_file(self, path):
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

    def _save_dataframes(self, df):
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

    def _load_csv(self, path):
        with open(path) as f:
            for i, row in enumerate(f):
                if row.startswith("Datum;"):
                    df = pandas.read_csv(filepath_or_buffer=path, sep=";", skiprows=i)

                    df = self._clean_columns(df)

                    df.insert(0, "time", df["Datum"] + ":" + df["Tid (UTC)"].str[:2])
                    df = df.drop(columns=["Datum", "Tid (UTC)"])
                    self._save_dataframes(df)
                    break
        self._get_unit_from_file(path)

    def _find_and_get(self, node, find, get):
        try:
            return node.find(find).attrib.get(get)
        except Exception as e:
            print(e)
            return None

    def _load_xml(self, path):
        with open(path) as f:
            xtree = et.parse(f)

        xroot = xtree.getroot()

        root = xroot.find("forecast").find("tabular")
        rows = []
        for node in root:
            time = node.attrib.get("from")
            persc = self._find_and_get(node, "precipitation", "value")
            windd = self._find_and_get(node, "windDirection", "deg")
            winds = self._find_and_get(node, "windSpeed", "mps")
            temp = self._find_and_get(node, "temperature", "value")
            pressure = self._find_and_get(node, "pressure", "value")

            rows.append({"time": time, "precipitation": persc, "windDirection": windd,
                         "windSpeed": winds, "temperature": temp, "pressure": pressure})

        df = pandas.DataFrame(rows, columns=[
            "time", "precipitation", "windDirection", "windSpeed", "temperature", "pressure"])

        df["time"] = df["time"].str.replace(r"[T]", ":")
        df["time"] = df["time"].str[:13]
        self._save_dataframes(df)

    def _load_json(self, path):
        with open(path) as f:
            json_file = json.load(f)

        rows = []

        for time in json_file.get("timeSeries"):
            row = {}
            row["time"] = time.get("validTime")
            categories = ["time"]
            for parameter in time.get("parameters"):
                name = parameter.get("name")
                unit = parameter.get("unit")
                value = parameter.get("values")[0]
                row[name] = value
                self._cat_unit[name] = unit
                if name not in categories:
                    categories.append(name)
            rows.append(row)

        df = pandas.DataFrame(rows, columns=categories)
        df["time"] = df["time"].str.replace(r"[T]", ":")
        df["time"] = df["time"].str[:13]

        self._save_dataframes(df)

    def load_dataframe(self, path):
        """load_dataframe reads path csv file and adds it as a dataframe into self.dataframes.

        Args:
            path (string): the path to the csv file.
        """
        try:
            if path.endswith(".csv"):
                self._load_csv(path)
            elif path.endswith(".xml"):
                self._load_xml(path)
            elif path.endswith(".json"):
                self._load_json(path)
        except Exception as e:
            print(e)
            return -1

    @property
    def categories(self):
        return self._categories

    def get_unit(self, category):
        try:
            return self._cat_unit[category]
        except:
            return ""

    def get_category(self, category):
        if type(category) is str:
            return self._get_single(category)
        elif type(category) is list and len(category) > 1:
            return self._get_multiple(category)
        else:
            raise TypeError("get_category only supports string or list objects > 1")

    def _get_single(self, category):
        if category not in self._categories:
            return -1

        for frame in self._dataframes:
            if category in frame.columns:
                return frame

    def _create_multi_frame(self, categories):
        dataframes = []

        for cat in categories:
            dataframes.append(self._get_single(cat))

        multi = dataframes.pop(0)
        for frame in dataframes:
            multi = multi.merge(frame, how="outer", on="time")
        multi = multi.sort_values(by=["time"])
        multi = multi.replace({np.nan: None})
        return multi

    def _get_multiple(self, categories):
        multi = self._create_multi_frame(categories)

        multi_data = []

        for cat in multi.columns:
            if cat != "time":
                multi_data.append(pandas.concat([multi["time"], multi[cat]], axis=1))

        return multi_data

    def export(self, category):
        if type(category) is str:
            df = self._get_single(category)
        elif type(category) is list and len(category) > 1:
            df = self._create_multi_frame(category)
        else:
            raise TypeError("get_category only supports string or list objects > 1")

        return df.to_csv()

if __name__ == "__main__":
    dm = DataManager()

    dm.load_dataframe("downloads\data.json")
    dm.load_dataframe(r"downloads\forecast_hour_by_hour.xml")

    print(dm.get_category("t"))
    print(dm.get_category("temperature"))