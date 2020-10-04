""""
- This file is used for resampling data monthly.
- Original data will record in each 10 seconds or 1 minute
- MySQL query group by day
- Resampling data will resample the query data to be monthly
- This file will operate monthly at the end of month, eg. 31 January at 11:59PM
- This will insert to table: month_data
"""
import sys# testing

import connectToDatabase as connect
import pandas as pd
from datetime import datetime
import logging

TABLE_NAME_DATA_MONTH = "month_data"
# MONTH = datetime.today().month -1
MONTH = datetime.today().month -2
YEAR = datetime.today().year



""""
- Replace empty data(string) with NaN
- convert data type to numeric
- Fill missing values by applying interpolate function:
    y2 is missing, y2 = (y3+y1)/2
"""
"""" COMMENT
This loop through all MeterId:
1 get one meterID and use it to get all data within particular month
2 use resampling function to fill NaN values and resample to be in month
3 insert data in month format to month_data table that will be used in forecasting
"""


def get_meter_data(meter_id_in, meter_data_in, mydb_connection):
    meter_data_in['ReadAt'] = pd.to_datetime(meter_data_in['ReadAt'])
    meter_data_in.rename(columns={'ReadAt': 'usage_date'}, inplace=True)
    meter_data_in.set_index('usage_date', inplace=True)

    meter_data_in['KWH'] = pd.to_numeric(meter_data_in['KWH'])
    meter_data_in.interpolate(method='linear', inplace=True)
    meter_data_diff = meter_data_in.diff()
    data_in_month = meter_data_diff.resample('M').sum()
    data_in_month['MeterId'] = int(meter_id_in)
    print(data_in_month)
    connect.insert_to_database(data_in_month, mydb_connection, TABLE_NAME_DATA_MONTH)


if __name__ == "__main__":
    mydb_sqlalchemy = connect.database_connection_with_sqlalchemy()
    sql_query_get_meter_id = "SELECT MeterId FROM Meter"
    MeterID = connect.read_from_database(sql_query_get_meter_id, mydb_sqlalchemy)
    meter_id_to_array = MeterID.values.reshape(-1, ).tolist()
    for meter_id in meter_id_to_array:
        try:
            sql_query_get_meter_data = "SELECT MAX(KWH) AS KWH, DATE_FORMAT(ReadAt, \"%Y-%m-%d 00:00:00\") AS ReadAt " \
                                       "FROM MeterData WHERE MeterId={0} AND YEAR(ReadAt)={1} AND MONTH(ReadAt)={2} " \
                                       "GROUP BY ReadAt, YEAR(ReadAt), MONTH(ReadAt), DAY(ReadAt)".format(meter_id,
                                                                                                          YEAR, MONTH)
            meter_data = connect.read_from_database(sql_query_get_meter_data, mydb_sqlalchemy)

            print(meter_data)


            get_meter_data(meter_id, meter_data, mydb_sqlalchemy)
        except Exception as err:
            logging.basicConfig(filename="Error_at_resample_data_log.log", filemode='w',
                                format='%(asctime)s - %(levelname)s - %(message)s')
            logging.error("Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))


