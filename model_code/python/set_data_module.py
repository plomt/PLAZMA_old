"""
MODULE LOAD RESULTS (TRAIN FOR MODEL) DATA FROM SERPENT FILES
"""
import os
from collections import namedtuple

import serpentTools
import pandas as pd
from typing import Tuple
from tqdm import tqdm

from logging_module import get_logger
from utils import (
    Configuration,
    load_to_postgres,
    get_postgres_connection,
)

os.environ['CONFIG_PATH'] = r"C:\Users\pavel\PycharmProjects\UIR\model_code\settings\settings.yml"
conf = Configuration()

DATA_PATH = conf["PATHS"]["DATA_PATH"]
TABLE_NAME = conf["TABLENAMES_POSTGRES"]["data"]
TEMPERATURES = [300, 2334, 8438, 10473, 16577, 18612, 24716, 26751, 32855, 34889, 40993, 43028,
                49132, 51167, 57271, 59306, 65410, 67444, 73548, 75583, 81687, 83722, 89826, 91861, 97964]
NUCLIDES = [10020, 10030, 20030]
REACTIONS = [102, 103]
UNIVERSE = '101'
logger = get_logger("set data")


def fast_warm(val) -> Tuple[list, list]:
    val_f = [val[i][1] for i in range(len(val))]
    val_w = [val[i][2] for i in range(len(val))]
    return val_f, val_w


def set_data(nuclide: int, reaction):
    """values for different temperatures"""
    nuclide_val = []

    files = os.listdir(DATA_PATH)
    for file in tqdm(files):
        mdx = serpentTools.read(DATA_PATH + "\\" + file)

        vals, unc = mdx.getXS(universe=UNIVERSE, isotope=nuclide, reaction=reaction)
        nuclide_val.append(vals)

    nuclide_reaction_f, nuclide_reaction_w = fast_warm(nuclide_val)
    return nuclide_reaction_f, nuclide_reaction_w


def data_to_db(nuclide: int):
    DBtable = namedtuple('DBtable', ['nuclide',
                                     'temperature',
                                     'reaction',
                                     'values_102_f',
                                     'values_102_w',
                                     'values_103_f',
                                     'values_103_w'
                                     ])
    size = len(TEMPERATURES)
    return DBtable(nuclide = [nuclide] * size,
            temperature = TEMPERATURES,
            reaction = [102] * size,
            values_102_f = set_data(nuclide, 102)[0],
            values_102_w = set_data(nuclide, 102)[1],
            values_103_f = set_data(nuclide, 103)[0],
            values_103_w = set_data(nuclide, 103)[1],
    )


def set_data_function():
    LIST_DATA = []
    for nuclide in NUCLIDES:
        LIST_DATA.append(
            data_to_db(nuclide)
        )

    d = {
        "nuclide": [],
        "temperature": [],
        "reaction_102_fast": [],
        "reaction_103_fast": [],
        "reaction_102_warm": [],
        "reaction_103_warm": []
    }

    for table in LIST_DATA:
        for i in range(len(TEMPERATURES)):
            d['nuclide'].append(table.nuclide[i])
            d['temperature'].append(table.temperature[i])
            d['reaction_102_fast'].append(table.values_102_f[i])
            d['reaction_103_fast'].append(table.values_103_f[i])
            d['reaction_102_warm'].append(table.values_102_w[i])
            d['reaction_103_warm'].append(table.values_103_w[i])

    df = pd.DataFrame(d)
    conn = get_postgres_connection()
    load_to_postgres(conn, df, TABLE_NAME)
    conn.close()
