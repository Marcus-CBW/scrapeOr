import sys
print(sys)

import mysql.connector
from mysql.connector import Error

def check_mysql_installed():
    try:
        # Try connecting to the MySQL server (adjust host, user, and password as needed)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Provide the correct MySQL root password
        )
        if connection.is_connected():
            print("MySQL is installed and running!")
        connection.close()

    except Error as e:
        # Handle connection errors
        if "Can't connect to MySQL" in str(e):
            print("MySQL is either not installed or the service isn't running.")
        else:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    check_mysql_installed()
