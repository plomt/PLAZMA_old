import os

from argparse_module import parser
from logging_module import get_logger
from utils import (
    Configuration,
    load_from_postgres_query,
    is_table_exists,
)
from create_tables_module import create_table
from drop_tables_module import drop_table
from machine_learning_model import machine_learning_model_main
from get_data_module import get_test_function
from set_data_module import set_data_function


os.environ['CONFIG_PATH'] = r"C:\Users\pavel\PycharmProjects\UIR\model_code\settings\settings.yml"

conf = Configuration()
CREATE_TABLE_DATA_SCRIPT = conf["PATHS"]["SCRIPTS_PATH"]
DROP_TABLE_DATA_SCRIPT = conf["PATHS"]["SCRIPTS_PATH"]
CREATE_TABLES_SCRIPTS = ["create_data.sql", "create_predictions.sql"]
DROP_TABLES_SCRIPTS = ["drop_data.sql", "drop_predictions.sql"]
TABLES_NAMES = [conf["TABLENAMES_POSTGRES"]["data"], conf["TABLENAMES_POSTGRES"]["predicts"]]

arguments = parser()
nuclide = arguments.nuclide
metric = arguments.metric
temperature = arguments.temperature

logger = get_logger("main")


class MainModel():

    @staticmethod
    def create_tables():
        for table in CREATE_TABLES_SCRIPTS:
            create_table(CREATE_TABLE_DATA_SCRIPT + "\\" + table)

    @staticmethod
    def drop_tables():
        for table in DROP_TABLES_SCRIPTS:
            drop_table(DROP_TABLE_DATA_SCRIPT + "\\" + table)

    def check_exists_tables(self, tablenames: list) -> bool:
        for tablename in tablenames:
            if not is_table_exists(tablename):
                return False
        return True

    def add_train_data(self):
        logger.info("add: start create tables")
        self.create_tables()
        logger.info("add: finish create tables")

        logger.info("add: start check exists tables")
        if not self.check_exists_tables(TABLES_NAMES):
            logger.error(f"One of the table does not exist")
            exit(1)
        logger.info("add: finish check exists tables")

        logger.info("add: start to add data to db")
        set_data_function()
        logger.info("add: finish to add data to db")

    def run_prediction(self):
        logger.info("run: start create tables")
        self.create_tables()
        logger.info("run: finish create tables")

        logger.info("run: start check exists tables")
        if not self.check_exists_tables(TABLES_NAMES):
            logger.error(f"One of the table does not exist")
            exit(1)
        logger.info("run: finish check exists tables")

        logger.info(f"run: start load data from Database for nuclide: {nuclide}")
        query = f"""SELECT * 
                    FROM {TABLES_NAMES[0]}
        """
        data = load_from_postgres_query(query)
        logger.info(f"run: finish load data from Database for nuclide {nuclide}")

        logger.info(f"run: start create test data for nuclide {nuclide} and temperature {temperature}")
        X_test = get_test_function(nuclide, temperature)
        logger.info(f"run: finish create test data for nuclide {nuclide} and temperature {temperature}")

        logger.info(f"run: start machine learning model with metric {metric}")
        machine_learning_model_main(metric=metric, X_test=X_test, data=data)
        logger.info(f"run: finish machine learning model with metric {metric}")



if __name__ == "__main__":
    mainModel = MainModel()

    mainModel.add_train_data()
    mainModel.run_prediction()
