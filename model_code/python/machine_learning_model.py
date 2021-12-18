import os

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from logging_module import get_logger
from utils import (
    Configuration,
    get_postgres_connection,
    load_to_postgres,
)

FILENAME_SCRIPT = ""

logger = get_logger("machine learning model")
os.environ['CONFIG_PATH'] = r"C:\Users\pavel\PycharmProjects\UIR\model_code\settings\settings.yml"
conf = Configuration()
POSTGRES_TABLENAMES = conf["TABLENAMES_POSTGRES"]


def choose_data_nuclide(nuclide: int, reaction: str, data: pd.DataFrame):
    data_nuclide = data[data['nuclide'] == nuclide]
    X_nuclide, y_nuclide = data_nuclide[['nuclide', 'temperature']], data_nuclide[reaction]

    X_nuclide_new = pd.DataFrame()
    X_nuclide_new['nuclide'] = X_nuclide['nuclide'].astype(str)
    X_nuclide_new['temperature'] = X_nuclide['temperature']
    X_nuclide_new = pd.get_dummies(X_nuclide_new)
    return X_nuclide_new, y_nuclide


def find_best_params(pipe, metric: str, reaction: str, nuclide: int, X_train, y_train):
    poly_degrees = [1, 2, 3, 4, 5, 6, 7]
    param_grid = [{'poly__degree': poly_degrees}]
    gs = GridSearchCV(estimator=pipe,
                      param_grid=param_grid,
                      scoring=metric,
                      cv=10,
                      n_jobs=-1)
    gs = gs.fit(X_train, y_train)
    logger.info("Best score of METRIC {} for model: NUCLIDE {}, REACTION {}: {}".format(metric, nuclide, reaction, -gs.best_score_))

    return gs.best_estimator_, -gs.best_score_


def train_best_model(best_estimator, X_train, y_train):
    clf = best_estimator
    clf.fit(X_train, y_train)
    return clf


def predict(model, X):
    return model.predict(X)


def process_find_train_predict(pipe, metric: str, reaction: str, nuclide: int, X_train, y_train, X):
    best_estimator, best_score = find_best_params(pipe, metric, reaction, nuclide, X_train, y_train)
    model = train_best_model(best_estimator, X_train, y_train)
    y_pred = predict(model, X)
    return y_pred, best_score


def machine_learning_model_main(metric, X_test, data):
    """
    Make prediction and save it in Database

    Parameters:
        metric: str -> accuracy, f1, recall, precision...
        X_test: dict -> {'nuclide': , 'temperature': }
    """
    nuclide, temperature = X_test['nuclide'][0], X_test['temperature'][0]

    pipe = Pipeline([('scaler', StandardScaler()),
                     ('poly', PolynomialFeatures()),
                     ('reg', LinearRegression()),
                     ])

    # reaction_102_fast
    X_102f, y_102f = choose_data_nuclide(nuclide, 'reaction_102_fast', data)
    # reaction_103_fast
    X_103f, y_103f = choose_data_nuclide(nuclide, 'reaction_103_fast', data)
    # reaction_102_warm
    X_102w, y_102w = choose_data_nuclide(nuclide, 'reaction_102_warm', data)
    # reaction_103_warm
    X_103w, y_103w = choose_data_nuclide(nuclide, 'reaction_103_warm', data)

    X_train_102f, X_test_102f, y_train_102f, y_test_102f = train_test_split(X_102f, y_102f, test_size=0.2)
    X_train_103f, X_test_103f, y_train_103f, y_test_103f = train_test_split(X_103f, y_103f, test_size=0.2)
    X_train_102w, X_test_102w, y_train_102w, y_test_102w = train_test_split(X_102w, y_102w, test_size=0.2)
    X_train_103w, X_test_103w, y_train_103w, y_test_103w = train_test_split(X_103w, y_103w, test_size=0.2)

    y_pred_102f, score_102f = process_find_train_predict(pipe=pipe, metric=metric, reaction='102f', nuclide=nuclide,
                                             X_train=X_train_102f, y_train=y_train_102f, X=X_test_102f)
    y_pred_103f, score_103f = process_find_train_predict(pipe=pipe, metric=metric, reaction='103f', nuclide=nuclide,
                                             X_train=X_train_103f, y_train=y_train_103f, X=X_test_103f)
    y_pred_102w, score_102w = process_find_train_predict(pipe=pipe, metric=metric, reaction='102w', nuclide=nuclide,
                                             X_train=X_train_102w, y_train=y_train_102w, X=X_test_102w)
    y_pred_103w, score_103w = process_find_train_predict(pipe=pipe, metric=metric, reaction='103w', nuclide=nuclide,
                                             X_train=X_train_103w, y_train=y_train_103w, X=X_test_103w)

    predictions_dict = {
        "nuclide": nuclide,
        "temperature": temperature,
        "reaction_102_fast": y_pred_102f,
        "reaction_103_fast": y_pred_103f,
        "reaction_102_warm": y_pred_102w,
        "reaction_103_warm": y_pred_103w,
        "metric_value_102_fast": score_102f,
        "metric_value_103_fast": score_103f,
        "metric_value_102_warm": score_102w,
        "metric_value_103_warm": score_103w
    }

    predictions_df = pd.DataFrame(predictions_dict)
    conn = get_postgres_connection()
    load_to_postgres(conn, predictions_df, POSTGRES_TABLENAMES["predicts"])
    conn.close()


if __name__ == '__main__':
    pass
