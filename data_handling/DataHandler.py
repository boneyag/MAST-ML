import numpy as np
import copy
from SingleFit import timeit
from DataParser import FeatureNormalization
from DataParser import FeatureIO
__author__ = "Tam Mayeshiba"

class DataHandler():
    """Data handling class
        (Combines old data_parser functionality with new DataParser methods)

    Args:
        data <pandas dataframe>
        input_data <pandas dataframe>: X data (input data)
        target_data <pandas dataframe>: y data (target data)
        input_features <list of str>: x features (input features)
        target_feature <str>: y feature (target feature)
                (the above five as parsed from DataParser)
        target_error_feature <str>: error in y feature (target error feature)
        labeling_features <list of str>: features to help identify data in
                                            plots

    Returns:
    Raises:
        ValueError if dataframe is None
    """
    def __init__(self, data=None, 
                    input_data=None, 
                    target_data=None, 
                    input_features=None, 
                    target_feature=None,
                    target_error_feature=None,
                    labeling_features=None,
                    grouping_feature=None):
        """Data Handler
            
        Attributes:
            #Set by keyword
            self.data <dataframe>: Main dataframe; all data
            self.data_unfiltered <dataframe>: Main dataframe; all data
                                                (archive in case of filters)
            self.input_data <dataframe>: Input data
            self.target_data <dataframe>: Target data
            self.input_features <list of str>: Input features
            self.target_feature <str>: Target feature
            self.target_error_feature <str>: Target error feature
            self.labeling_features <list of str>: Labeling features
            self.grouping_feature <str>: Grouping feature
            #Set in code
            self.target_error_data <dataframe>
            self.target_prediction <dataframe>
            self.groups <list>: list of groups from self.grouping_feature
            self.group_data <dataframe>: Grouping data feature
        """
        if data is None:
            raise ValueError("No dataframe.")
        #Set by keyword
        self.data = copy.deepcopy(data)
        self.data_unfiltered = copy.deepcopy(data)
        self.input_data = copy.deepcopy(input_data)
        self.target_data = copy.deepcopy(target_data)
        self.input_features = list(input_features)
        self.target_feature = target_feature
        self.target_error_feature = target_error_feature
        if labeling_features is None:
            self.labeling_features = labeling_features
        else:
            self.labeling_features = list(labeling_features)
        self.grouping_feature = grouping_feature
        #Set in code
        self.target_error_data = None
        self.target_prediction = None
        self.group_data = None
        self.groups = None
        #Run upon initialization
        self.set_up_data()
        return

    def set_up_data(self):
        if not (self.target_error_feature is None):
            self.target_error_data = self.data[self.target_error_feature]
        if not (self.grouping_feature is None):
            self.group_data = self.data[self.grouping_feature]
            self.groups = np.unique(self.group_data)
        return


    def set_up_data_from_features(self):
        """To reset data, for example, if self.data has been changed
            by filtering
        """
        self.set_up_data() #repeat set up
        self.input_data = self.data[self.input_features]
        self.target_data = self.data[self.target_feature]
        if "Prediction" in self.data.columns:
            self.target_prediction = self.data["Prediction"]
        return

    def add_prediction(self, prediction_data):
        fio = FeatureIO(self.data)
        self.data = fio.add_custom_features(["Prediction"], prediction_data)
        self.target_prediction = self.data["Prediction"]
        return

    def add_filters(self, filter_list):
        for (feature, operator, threshold) in filter_list:
            fio = FeatureIO(self.data)
            self.data= fio.custom_feature_filter(feature,operator,threshold)
        self.set_up_data_from_features()
        return

    def print_data(self, csvname="data.csv"):
        cols = list()
        if not self.labeling_features is None:
            cols.extend(self.labeling_features)
        if not self.grouping_feature is None:
            if not (self.grouping_feature in self.labeling_features):
                cols.extend(self.grouping_feature)
        cols.extend(self.input_features)
        if not self.target_data is None:
            cols.append(self.target_feature)
        if not self.target_error_feature is None:
            cols.append(self.target_error_feature)
        if not self.target_prediction is None:
            cols.append("Prediction")
        self.data.to_csv(csvname,
                        columns=list(cols))
        return cols