import sys
import mysql.connector
import pandas as pd
import sqlalchemy

# --------- Database Configuration ---------
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'meterdb-dev'
DB_USER = 'root'
DB_PASSWORD = 'root'

# --------- End Database Configuration ---------

""""
########### Read From File For Testing ###########
predicted_data = pd.read_csv("predicteddata.csv", infer_datetime_format=True, index_col=['FutureDateMonth'])
predicted_data['KWH'] = pd.to_numeric(predicted_data['KWH'])
predicted_data['MeterID'] = 98801006
########### Read From File For Testing ###########
"""


def database_connection_with_sqlalchemy():
    try:
        mydb_sqlalchemy = sqlalchemy.create_engine(
            'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME),
            echo=False)
        print("Succeed sqlalchemy")
        return mydb_sqlalchemy
    except Exception as ex:
        template_message = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template_message.format(type(ex).__name__, ex.args)
        print(message)
        sys.exit()


"""Table Structure
month_data = \"""CREATE TABLE IF NOT EXISTS month_data (
                                      MeterID INT,
                                      usage_date DATETIME,
                                      KWH FLOAT,
                                      FOREIGN KEY (MeterID) REFERENCES Meter(MeterID)
                                      )\"""
                                      

NEW                                  
prediction_table = \"""CREATE TABLE IF NOT EXISTS prediction_table (
                                      AreaID INT NOT NULL,
                                      predicted_at DATETIME DEFAULT NULL,
                                      minimum_KWH FLOAT DEFAULT NULL,
                                      KWH FLOAT DEFAULT NULL,
                                      maximum_KWH FLOAT DEFAULT NULL,
                                      prediction_date DATETIME NOT NULL,
                                      FOREIGN KEY (AreaID) REFERENCES ServiceArea(AreaID)
                                      )\"""
                                      

  """

"""
Need to check the insert query and send log info. to Admin when error occurs or too many attempts
"""


def read_from_database(sql_query, con):
    try:
        read_data = pd.read_sql(sql=sql_query, con=con)
        return read_data
    except Exception as ex:
        template_message = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template_message.format(type(ex).__name__, ex.args)
        print(message)


def insert_to_database(data, mydb_sqlalchemy, tablename):
    try:
        data.to_sql(con=mydb_sqlalchemy, name=tablename, if_exists='append')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


# Testing Purpose
# try:
#     # df = pd.read_sql_table("meter", database_connection_with_sqlalchemy(predicted_data))
# mydb_sqlalchemy = database_connection_with_sqlalchemy()
#     test = pd.read_sql("Select * from meter", mydb_sqlalchemy)
#     print(test)
#     # insert_to_database(predicted_data, mydb_sqlalchemy)
# except Exception as e:
#     print(e)
