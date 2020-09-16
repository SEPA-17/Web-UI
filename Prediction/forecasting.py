import logging
import sys
from itertools import product
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from statsmodels.tsa.arima_model import ARIMA
import connectToDatabase as connect
from datetime import datetime
import time
import warnings
# import matplotlib.pyplot as plt # testing

warnings.filterwarnings('ignore')

# ALL lines end with # testing, used for testing only

# --------- Configuration ---------
""""
Set p, d, q value for ARIMA
p for AR
d forx I
q for MA
"""
P = Q = range(5, 9)
D = range(2, 5)
PARAMETERS = product(P, D, Q)
PARAMETERS_LIST = list(PARAMETERS)
TODAY = datetime.today()
TABLE_NAME = "prediction_table"


# --------- End Configuration ---------

def get_service_area_id(mydb_connection):
    sql_query_get_area_id = "Select AreaID from servicearea"
    area_id = connect.read_from_database(sql_query_get_area_id, mydb_connection)
    area_id_to_array = area_id.values.reshape(-1, ).tolist()
    return area_id_to_array


def get_meter_id(mydb_connection, areaID):
    sql_query_get_meter_id = "Select MeterID from meter WHERE AreaID={0}".format(int(areaID))
    meter_id = connect.read_from_database(sql_query_get_meter_id, mydb_connection)
    print("In get_meter_id function")# testing
    print(meter_id)# testing
    print(meter_id.shape)# testing
    meter_id_to_array_in = meter_id.values.reshape(-1, ).tolist()
    return meter_id_to_array_in


def get_meter_data(p_meter_id_to_array, mydb_connection):
    sql_query_get_meter_data = "SELECT usage_date, KWH FROM month_data WHERE MeterID IN {0}".format(tuple(p_meter_id_to_array))
    meter_data = connect.read_from_database(sql_query_get_meter_data, mydb_connection)
    meter_data_log_in = resample_data(meter_data)
    print(meter_data_log_in)# testing
    return meter_data_log_in


def resample_data(meter_data):
    meter_data.set_index('usage_date', inplace=True)
    meter_data = meter_data.resample('M').sum()
    meter_data_log_in = np.log(meter_data)
    meter_data_log_in.dropna(inplace=True)
    return meter_data_log_in


def optimize_ARIMA(parameters_list, meter_data):
    best_aic = float('inf')
    list = None #testing
    global best_model
    for param in parameters_list:
        try:
            model = ARIMA(meter_data, order=(param[0], param[1], param[2]))
            # model = ARIMA(meter_data, order=(8,1,5)) #testing
            aic = model.fit().aic
        except Exception as ex:
            # template_message = "An exception of type {0} occurred. Arguments:\n{1!r}"# testing
            # message = template_message.format(type(ex).__name__, ex.args)# testing
            # print(message)# testing
            continue

        if aic < best_aic:
            best_aic = aic
            best_model = model
            list = [param[0], param[1], param[2]] #testing
        # break #testing
    print("##########################################################")# testing
    print(list)# testing
    return best_model


def reform_predicted_data(metadata, result_data_in):
    minimum_result_data_list = []
    maximum_result_data_list = []
    result_data_list = result_data_in[0].tolist()

    # Minimum and maximum of future data
    for x, y in result_data[2]:
        minimum_result_data_list.append(x)
        maximum_result_data_list.append(y)

    last_of_the_month = metadata.index[-1] + relativedelta(months=+1)
    # last_of_the_month = parser.parse(last_of_the_month)# testing
    next_12_months = metadata.index[-1] + relativedelta(months=+12)
    # next_12_months = parser.parse(next_12_months)# testing
    next_12_months_rng = pd.date_range(start=last_of_the_month, end=next_12_months, freq='M')
    future_meter_data = pd.DataFrame(next_12_months_rng, columns=['prediction_date'])
    future_meter_data['KWH'] = result_data_list
    future_meter_data['minimum_KWH'] = minimum_result_data_list
    future_meter_data['maximum_KWH'] = maximum_result_data_list
    future_meter_data = future_meter_data.set_index('prediction_date')
    future_meter_data = np.exp(future_meter_data)
    print(future_meter_data)# testing

    return future_meter_data


if __name__ == "__main__":
    try:
        start_time = time.time()# testing
        mydb_sqlalchemy = connect.database_connection_with_sqlalchemy()
        areaID_to_array = get_service_area_id(mydb_sqlalchemy)
        for areaId in areaID_to_array:
            meter_id_to_array = get_meter_id(mydb_sqlalchemy, areaId)
            meter_data_log = get_meter_data(meter_id_to_array, mydb_sqlalchemy)
            before_arima_prediction = time.time()# testing
            # Start Prediction
            best_model = optimize_ARIMA(PARAMETERS_LIST, meter_data_log)
            after_arima_prediction = time.time()# testing
            results_ARIMA = best_model.fit()
            # results_ARIMA.plot_predict('2007', '2012')# testing
            result_data = results_ARIMA.forecast(steps=12)

            future_data = reform_predicted_data(meter_data_log, result_data)
            # sys.exit()# testing
            future_data['AreaID'] = areaId
            future_data['predicted_at'] = TODAY
            connect.insert_to_database(future_data, mydb_sqlalchemy, TABLE_NAME)
            finish_time = time.time()# testing
            print("Program start to before ARIMA prediction: % s seconds" % (before_arima_prediction - start_time))# testing
            print("ARIMA prediction function: % s seconds" % (after_arima_prediction - before_arima_prediction))# testing
            print("Program start to after ARIMA prediction: % s minutes" % ((after_arima_prediction - start_time)/60))# testing
            print("Program start to end program: % s minutes" % ((finish_time - start_time)/60))# testing
            break# testing
    except Exception as err:
        logging.basicConfig(filename="Error_at_forecasting_log.log", filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error("Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))
        sys.exit()
