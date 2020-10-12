import logging
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
import connectToDatabase as connect
from datetime import datetime
import pmdarima as pm
import warnings

warnings.filterwarnings('ignore')

# --------- Configuration ---------
""""
Set p, d, q value for ARIMA
p for AR
d forx I
q for MA
"""
START_p = 0
START_q = 0
MAX_p = 50
MAX_d = 20
MAX_q = 40
M = 12
START_OF_PROGRAM = datetime.today()
TABLE_NAME = "prediction_table"
# --------- End Configuration ---------


def get_service_area_id(mydb_connection):
    sql_query_get_area_id = "Select AreaId from ServiceArea"
    area_id = connect.read_from_database(sql_query_get_area_id, mydb_connection)
    area_id_to_array = area_id.values.reshape(-1, ).tolist()
    return area_id_to_array


def get_meter_id(mydb_connection, areaID):
    sql_query_get_meter_id = "Select MeterId from Meter WHERE AreaId={0}".format(int(areaID))
    meter_id = connect.read_from_database(sql_query_get_meter_id, mydb_connection)
    meter_id_to_array_in = meter_id.values.reshape(-1, ).tolist()
    return meter_id_to_array_in


def get_meter_data(meter_id_to_array_in, mydb_connection):
    sql_query_get_meter_data = "SELECT usage_date, KWH FROM month_data WHERE MeterId IN {0}".format(tuple(meter_id_to_array_in))
    meter_data = connect.read_from_database(sql_query_get_meter_data, mydb_connection)
    meter_data_log_in = resample_data(meter_data)
    return meter_data_log_in


def resample_data(meter_data):
    meter_data.set_index('usage_date', inplace=True)
    meter_data = meter_data.resample('M').sum()
    meter_data_log_in = np.log(meter_data)
    meter_data_log_in.dropna(inplace=True)
    return meter_data_log_in


def optimize_ARIMA(meter_data):
    best_model_in = pm.auto_arima(meter_data, start_p=START_p, start_q=START_q, max_p=MAX_p, max_d=MAX_d, max_q=START_q, error_action='warn', m=M)
    return best_model_in


def reform_predicted_data(metadata, result_data_in, conf_int_in):
    minimum_result_data_list = []
    maximum_result_data_list = []
    result_data_list = result_data_in.tolist()

    # Minimum and maximum of future data
    for x, y in conf_int_in:
        minimum_result_data_list.append(x)
        maximum_result_data_list.append(y)

    last_of_the_month = metadata.index[-1] + relativedelta(months=+1)
    next_12_months = metadata.index[-1] + relativedelta(months=+12)
    next_12_months_rng = pd.date_range(start=last_of_the_month, end=next_12_months, freq='M')
    future_meter_data = pd.DataFrame(next_12_months_rng, columns=['prediction_date'])
    future_meter_data['minimum_KWH'] = minimum_result_data_list
    future_meter_data['KWH'] = result_data_list
    future_meter_data['maximum_KWH'] = maximum_result_data_list
    future_meter_data = future_meter_data.set_index('prediction_date')
    future_meter_data = np.exp(future_meter_data)
    return future_meter_data


def remove_old_prediction_data(mydb_connection, areaID):
    sql_query_remove_old_prediction = "Delete from {0} where AreaId = {1}".format(TABLE_NAME, areaID)
    conn = mydb_connection.connect()
    conn.execute(sql_query_remove_old_prediction)


if __name__ == "__main__":
    try:
        mydb_sqlalchemy = connect.database_connection_with_sqlalchemy()
        areaID_to_array = get_service_area_id(mydb_sqlalchemy)
        for areaId in areaID_to_array:
            meter_id_to_array = get_meter_id(mydb_sqlalchemy, areaId)
            meter_data_log = get_meter_data(meter_id_to_array, mydb_sqlalchemy)
            # Start Prediction
            best_model = optimize_ARIMA(meter_data_log)
            result_data, conf_int = best_model.predict(n_periods=12, return_conf_int=True, alpha=0.05)

            future_data = reform_predicted_data(meter_data_log, result_data, conf_int)

            future_data['AreaId'] = areaId
            future_data['predicted_at'] = datetime.today()
            remove_old_prediction_data(mydb_sqlalchemy, areaId)
            connect.insert_to_database(future_data, mydb_sqlalchemy, TABLE_NAME)
    except Exception as err:
        logging.basicConfig(filename="Error_at_forecasting_log.log", filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error("Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))

