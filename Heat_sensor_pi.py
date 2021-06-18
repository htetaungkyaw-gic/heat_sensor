import os
import sys
import glob
import time
import datetime
import socket
from mysql.connector import connect

# Initialize the GPIO Pins
os.system('modprobe w1-gpio')  # Turns on the GPIO module
os.system('modprobe w1-therm') # Turns on the Temperature module

# Finds the correct device file that holds the temperature data
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# A function that reads the sensors data
def read_temp_raw():
    f = open(device_file, 'r') # Opens the temperature device file
    lines = f.readlines() # Returns the text
    f.close()
    return lines

# Convert the value of the sensor into a temperature
def read_tempc():
    lines = read_temp_raw() # Read the temperature 'device file'

    # While the first line does not contain 'YES', wait for 0.2s
    # and then read the device file again.
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    # Look for the position of the '=' in the second line of the
    # device file.
    equals_pos = lines[1].find('t=')

    # If the '=' is found, convert the rest of the line after the
    # '=' into degrees Celsius, then degrees Fahrenheit
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

try:
    
    #sql_ip = socket.gethostbyname('GIC-LPT-0110.local')
    #sql_ip = socket.gethostbyname('raspberrypi')
    #sql_ip = "192.168.0.54"
    dbname='omron_env'
    sql_host='192.168.21.1'
    sql_user='root'
    sql_pass='1233'
    
    while True:
                                    
        device_name = "machine1R"
        idcode = device_name + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        time_measured = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        hrago = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y/%m/%d %H:%M:%S")
        temperatureC = round(read_tempc(), 2)
        
        sql = "INSERT INTO heatsensor(id,device_id,TemperatureC,time_measured) VALUES (%s, %s, %s, %s)"
        val = (idcode, device_name, temperatureC , time_measured)
        
        
        try:
            
            #mydb = connect(host=sql_ip,port=3306,user="root",password="1233",database="omron_env")
            mydb = connect(host=sql_host,port=3306,user = sql_user,password = sql_pass,database = dbname)
            mydb.autocommit = False
            mycursor = mydb.cursor()
                        
            mycursor.execute(sql, val)
            mydb.commit()
                  
            mycursor.close()
            mydb.close()
            
            
        except connect.Error as error:
            print("Failed to update record to database rollback: {}".format(error))
            # reverting changes because of exception
            mydb.rollback()

        time.sleep(4.5)

except Exception as e: 

    print(time_measured + "Exception: " + str(e)) 

    import traceback 

    traceback.print_exc()
    
    sensor.close()
    # closing database connection.
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("connection is closed")

    sys.exit(1) 

     

finally: 

     print("Exit" + time_measured)
     # closing database connection.
     if mydb.is_connected():
         mycursor.close()
         mydb.close()
         print("connection is closed")
     
     sys.exit(1)
