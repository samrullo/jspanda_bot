import os
import mysql.connector
from conf.mysql import get_mysql_db_info
import pandas as pd
import numpy as np
import datetime
from models.family_spending import FamilySpending
from utils.utils import get_logger

to_yyyymmdd = lambda x: datetime.datetime.strftime(x, '%Y%m%d')
_logger = get_logger()

m = FamilySpending()
# create received_money table if not exists
m.create_table()

# load received_money records
folder = r"C:\Users\amrul\Documents"
file = "familyspending.xlsx"
df = pd.read_excel(os.path.join(folder, file))
df = df.fillna(0)
_logger.info(f"loaded family spending dataframe {len(df)}")
df.columns = df.columns.map(lambda x: x.lower())

cols = df.columns.tolist()
for i, row in df.iterrows():
    date = row['month']
    _logger.info(f"adding cost items for the month {date}")
    for col in cols[1:]:
        name = col
        amount = row[col]
        m.add_item(date, name, amount)
        _logger.info(f"added {date} {name} {amount}")
