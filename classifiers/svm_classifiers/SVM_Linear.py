import os
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.svm import NuSVC
from sklearn.model_selection import GridSearchCV
from classifiers.Model import Model


dir_name = os.path.dirname(__file__)
data_path = os.path.join(dir_name, '../../preprocessed_data/team_seasons_classified_1.csv')




class SVMLinearModel(Model):
    def __init__(self):
        self.name = "Linear-Support SVC"
        self.model =  (SVC(kernel='linear',probability=True))

    def get_tuned_parameters(self,x,y):
        # data = pd.read_csv(data_path)
        # x = data.iloc[:, 3:-1]
        # y = data.iloc[:, -1]
        param_grid = {"C": [0.001, 0.01, 0.1, 1, 10, 20, 30, 40, 50, 100]}
        grid_search = GridSearchCV(LinearSVC(), param_grid, cv=10)
        grid_search.fit(x, y)
        print("Best parameters for LinearSVC:{}".format(grid_search.best_params_))



# class SVMLinearP001(Model):
#     def __init__(self):
#         self.name = "Linear-Support SVC"
#         self.model =  LinearSVC(C=0.001)



class SVMLinearP01(Model):
    def __init__(self):
        self.name = "Linear-Support SVC"
        self.model =  LinearSVC(C=0.01)


class SVMLinearP1(Model):
    def __init__(self):
        self.name = "Linear-Support SVC"
        self.model =  LinearSVC(C=0.1)

class SVMLinear10(Model):
    def __init__(self):
        self.name = "Linear-Support SVC"
        self.model =  LinearSVC(C=10)


class SVMLinear100(Model):
    def __init__(self):
        self.name = "Linear-Support SVC"
        self.model =  LinearSVC(C=100)





class TunedSVMLinearModel(Model):
    def __init__(self):
        self.name = "Linear-Support SVC Tuned"
        self.model = LinearSVC(C=20)


# get_tuned_parameters()


# class XGBoost(Model):
#     def __init(self):
#         self.name = "XGBoost"
#         self.model = xgb