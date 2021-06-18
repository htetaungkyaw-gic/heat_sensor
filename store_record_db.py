import sys
from mysql.connector import connect

def fetch_device_name(table_name):
    # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
    cnx = connect(
        host='localhost',
        database='omron_env',
        user='root',
        password=''
    )

    cursor = cnx.cursor()
    cursor.execute('SELECT DISTINCT device_id FROM ' + table_name)

    devices_id = cursor.fetchall()

    # Closing connection
    cnx.close()

    return devices_id
    
    
def move_table_data(device_id):
     # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
     try:
  
         mydb = connect(host="localhost",port=3306,user="root",password="",database="omron_env")
         mydb.autocommit = False
         mycursor = mydb.cursor()
         movesql = "call record('"+str(device_id)+"')"    
         mycursor.execute(movesql)
         mydb.commit()
                        
         mycursor.close()
         mydb.close()
                
            
     except connect.Error as error:
         print("Failed to update record to database rollback: {}".format(error))
         # reverting changes because of exception
         mydb.rollback()
         if mydb.is_connected():
             mycursor.close()
             mydb.close()
             print("connection is closed with error")





devices_id = fetch_device_name('heatsensor')


for device in devices_id:
     
     move_table_data(device[0])
     
      