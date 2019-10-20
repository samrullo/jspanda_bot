import os
import mysql.connector
from conf.mysql import get_mysql_db_info
import pandas as pd
import numpy as np
import datetime

to_yyyymmdd = lambda x: datetime.datetime.strftime(x, '%Y%m%d')

db = get_mysql_db_info()
mydb = mysql.connector.connect(**db)
mycursor = mydb.cursor()

# get tables
mycursor.execute("show tables")
tables = [x[0] for x in mycursor]

# create received_money table if not exists
if "received_money" not in tables:
    statement = "CREATE TABLE IF NOT EXISTS `received_money`(`id` INT AUTO_INCREMENT, `registered_date` DATE, `amount_usd` INT, `exchange_rate` FLOAT, `amount_jpy` INT, PRIMARY KEY (`id`))"
    mycursor.execute(statement)

# load received_money records
folder = r"C:\Users\amrul\Documents\japan_sweets_business"
file = "japansweet_business_hisob_kitob.xlsx"
df = pd.read_excel(os.path.join(folder, file))
df.drop(68, inplace=True)
df['date'] = pd.to_datetime(df['date'])
data_df = df[['date', 'income(in USD)', 'income']].copy()
data_df.columns = ['registered_date', 'amount_usd', 'amount_jpy']
data_df['registered_date'] = data_df['registered_date'].apply(to_yyyymmdd)
data_df['exchange_rate'] = data_df['amount_jpy'] / data_df['amount_usd']
print(f"Finished loading recived money : {len(data_df)}")

print(f"Will start inserting to table")
for i, row in data_df.iterrows():
    print(f"will insert {row.tolist()}")
    statement = "INSERT INTO received_money(`registered_date`,`amount_usd`,`exchange_rate`,`amount_jpy`) VALUES (%s,%s,%s,%s)"
    mycursor.execute(statement, row.tolist())
    mydb.commit()
    print(f"finished inserting {row.tolist()}")
