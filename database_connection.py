# # db_connect.py (or any other file where you need the address)
# import requests
# import psycopg2
# import minheap
#
# def get_college_address():
#     url = "http://127.0.0.1:5000/get_address"  # Flask API endpoint
#     try:
#         response = requests.get(url)
#         data = response.json()
#         print(data)
#         return data.get("college_address", "")
#     except requests.exceptions.RequestException as e:
#         print("Error fetching address:", e)
#         return ""
#
# def connect_db():
#     conn = psycopg2.connect(
#         dbname="your_db",
#         user="your_user",
#         password="your_password",
#         host="your_host",
#         port="your_port"
#     )
#     return conn
#
# def fetch_pg_data():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM pg_listings")  # Fetch all PG rows
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return rows
#
# # Example usage
# if __name__ == "__main__":
#     college_address = get_college_address()
#     print("Fetched College Address:", college_address)
#
#     # Now use it to calculate distances
#     pg_data = fetch_pg_data()
#     for row in pg_data:
#         node_address = row[3]  # Assuming address is the 4th column
#         print(f"PG Address: {node_address}, College Address: {college_address}")
from flask import Flask
import preference_flask as pf
import requests

app = Flask(__name__)

def get_college_address():
    url = "http://127.0.0.1:5000/get_address"  # Flask API endpoint
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("college_address", "")
    except requests.exceptions.RequestException as e:
        print("Error fetching address:", e)
        return ""

# Example usage
if __name__ == "__main__":
    with app.app_context():
        college_address = get_college_address()
        print("Fetched College Address:", college_address)