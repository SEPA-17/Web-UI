import logging
import sys
import pandas as pd
import sqlalchemy

# --------- Database Configuration ---------
DB_HOST = 'web-db.c6vnael0nhls.ap-southeast-2.rds.amazonaws.com'
DB_PORT = 3306
DB_NAME = 'main_DB'
DB_USER = 'detectivePretzel'
DB_PASSWORD = 'brunoDiplomat'

# --------- End Database Configuration ---------


def database_connection_with_sqlalchemy():
    try:
        mydb_sqlalchemy = sqlalchemy.create_engine(
            'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME),
            echo=False)
        print("Database Connection Successful")
        return mydb_sqlalchemy
    except Exception as err:
        logging.basicConfig(filename="Error_at_connectToDatabase_log.log", filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(
            "In database_connection_with_sqlalchemy function, Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))
        sys.exit()


"""Table Structure
month_data = \"""CREATE TABLE IF NOT EXISTS month_data (
                                      monthId int NOT NULL AUTO_INCREMENT,
                                      MeterId INT,
                                      usage_date DATETIME,
                                      KWH DOUBLE,
                                      FOREIGN KEY (MeterId) REFERENCES Meter(MeterId)
                                      )\"""
                                      

NEW                                  
prediction_table = \"""CREATE TABLE IF NOT EXISTS prediction_table (
                                      predictionId int NOT NULL AUTO_INCREMENT,
                                      AreaId INT NOT NULL,
                                      predicted_at DATETIME DEFAULT NULL,
                                      minimum_KWH DOUBLE DEFAULT NULL,
                                      KWH DOUBLE DEFAULT NULL,
                                      maximum_KWH DOUBLE DEFAULT NULL,
                                      prediction_date DATETIME NOT NULL,
                                      FOREIGN KEY (AreaId) REFERENCES ServiceArea(AreaId)
                                      )\"""
                                      

  """


def read_from_database(sql_query, con):
    try:
        read_data = pd.read_sql(sql=sql_query, con=con)
        return read_data
    except Exception as err:
        logging.basicConfig(filename="Error_at_connectToDatabase_log.log", filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(
            "In read_from_database function, Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))


def insert_to_database(data, mydb_sqlalchemy, tablename):
    try:
        data.to_sql(con=mydb_sqlalchemy, name=tablename, if_exists='append')
    except Exception as err:
        logging.basicConfig(filename="Error_at_connectToDatabase_log.log", filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(
            "In insert_to_database function, Type {0} occurred. Arguments:\n{1!r}".format(type(err).__name__, err.args))

