
import mysql.connector

def connect_to_database():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='jrk*j8WMpP87az*N',
        database='yatra'
    )
    if connection.is_connected():
        return connection

def validate_login(pan_number, login_name_value, password_value):
    connection = connect_to_database()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE Pancard_no = %s AND Name = %s AND Password = %s"
    cursor.execute(query, (pan_number, login_name_value, password_value))
    result = cursor.fetchone()
    
    if result:
        return True
    else:
        return False
    
    cursor.close()
    connection.close()
