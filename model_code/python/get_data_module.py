import pandas as pd

from logging_module import get_logger
from utils import (
    load_from_postgres_query,
    is_table_exists,
)

logger = get_logger("get data")

def get_data_function(nuclide: int, tablename: str):
    if is_table_exists(tablename):
        query = f"""
            SELECT *
            FROM {tablename}
            WHERE 'nuclide' = {nuclide}
        """
        ans = load_from_postgres_query(query)
    else:
        return None
    return ans


def get_test_function(nuclide: int, temperature: int):
    test_dict = {
        "nuclide": [nuclide],
        "temperature": [temperature]
    }
    return pd.DataFrame(test_dict)