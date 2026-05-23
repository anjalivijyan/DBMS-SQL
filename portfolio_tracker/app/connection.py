#connecting to sql 
import mysql.connector
import os 
from dotenv import load_dotenv 

load_dotenv(os.path.join(os.path.dirname(__file__), 'dbms.env'))

def get_connected_sql():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    