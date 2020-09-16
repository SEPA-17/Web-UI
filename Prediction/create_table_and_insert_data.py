import sys
import csv
import mysql.connector


# --------- Database Configuration ---------
DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'meterdb-dev'
DB_USER = 'root'
DB_PASSWORD = 'root'

# --------- End Database Configuration ---------


def Database_Connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD):
    try:
        mydb = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        sys.exit()
    return mydb


mydb = Database_Connection(DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
print(mydb)
print("Connect Succeed")

########################################
#Check table not exist, then create
mycursor = mydb.cursor()
sql_check_table_ServiceArea_not_exist_create = "CREATE TABLE IF NOT EXISTS ServiceArea (AreaID INT PRIMARY KEY, AreaName VARCHAR(255))"
mycursor.execute(sql_check_table_ServiceArea_not_exist_create)

sql_create_Meter = "CREATE TABLE IF NOT EXISTS Meter (MeterID INT UNIQUE, AreaID INT, FOREIGN KEY (AreaID) REFERENCES ServiceArea(AreaID))"
mycursor.execute(sql_create_Meter)

sql_check_table_MeterData_not_exist_create = """CREATE TABLE IF NOT EXISTS MeterData (
                                                ID INT AUTO_INCREMENT PRIMARY KEY,
                                                MeterID INT,
                                                ReadAt DATETIME,
                                                KWH FLOAT,
                                                KW FLOAT,
                                                KVA FLOAT,
                                                KVAr FLOAT,
                                                Ph1i FLOAT,
                                                Ph2i FLOAT,
                                                Ph3i FLOAT,
                                                Ph1v FLOAT,
                                                Ph2v FLOAT,
                                                Ph3v FLOAT,
                                                PF FLOAT,
                                                FOREIGN KEY (MeterID) REFERENCES Meter(MeterID)
                                                )"""
mycursor.execute(sql_check_table_MeterData_not_exist_create)


####################################
#For Global Active Power
sql_global_active_power = """CREATE TABLE IF NOT EXISTS Household_power (
                             ID INT AUTO_INCREMENT PRIMARY KEY,
                                                MeterID INT DEFAULT 98801006,
                                                ReadAt DATETIME,
                                                Global_active_power FLOAT,
                                                Global_reactive_power FLOAT,
                                                Voltage FLOAT,
                                                Global_intensity FLOAT,
                                                Sub_metering_1 FLOAT,
                                                Sub_metering_2 FLOAT,
                                                Sub_metering_3 FLOAT
                                                )"""
mycursor.execute(sql_global_active_power)


month_data = """CREATE TABLE IF NOT EXISTS month_data (
                                      MeterID INT,
                                      DateTime DATETIME,
                                      KWH FLOAT,
                                      FOREIGN KEY (MeterID) REFERENCES Meter(MeterID)
                                      )"""
mycursor.execute(month_data)


prediction_table = """CREATE TABLE IF NOT EXISTS prediction_table (
                                      AreaID INT NOT NULL,
                                      prediction_date DATETIME NOT NULL,
                                      KWH FLOAT DEFAULT NULL,
                                      predicted_at DATETIME DEFAULT NULL,
                                      FOREIGN KEY (AreaID) REFERENCES ServiceArea(AreaID)
                                      )"""
mycursor.execute(prediction_table)


from dateutil import parser
def insert_to_database_household(mydb, row):
    insert_sql = ("INSERT INTO Household_power "
                "(ReadAt,Global_active_power,Global_reactive_power,Voltage,Global_intensity,Sub_metering_1,Sub_metering_2,Sub_metering_3)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                )
    row[0] = parser.parse(row[0])
    cursor = mydb.cursor()
    cursor.execute(insert_sql, row)

    print(f'Insert to database {cursor.lastrowid}')


with open("testing_csv\household_data.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            insert_to_database_household(mydb, row)
        line_count += 1


    mydb.commit()
    print(f'Processed {line_count} lines')
#End Global Active Power
####################################



def insert_to_database(mydb, row):
    insert_sql = ("INSERT INTO MeterData "
                "(MeterID, ReadAt, KWH, KW, KVA, KVAr, Ph1i, Ph2i, Ph3i, Ph1v, Ph2v, Ph3v, PF)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )
    row[1] = parser.parse(row[1])
    cursor = mydb.cursor()
    cursor.execute(insert_sql, row)

    print(f'Insert to database {cursor.lastrowid}')




with open("testing_csv\sample_data.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            insert_to_database(mydb, row)
        line_count += 1
    mydb.commit()
    print(f'Processed {line_count} lines')
