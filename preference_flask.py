from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import minheap
import math
import requests

app = Flask(__name__)
CORS(app)

# Global variable to store the address
college_address = ""

# Database connection details
db_name = "postgres"
db_user = "postgres.nbwcvxybhyhtjzcyxjmn"
db_password = "1@Maghizh"
db_host = "aws-0-ap-south-1.pooler.supabase.com"
db_port = "6543"

@app.route('/save_address', methods=['POST'])
def save_address():
    global college_address
    data = request.json
    address = data.get("address")

    if address:
        college_address = address
        print("Received Address:", college_address)
    else:
        pass

    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        cur = conn.cursor()
        cur.execute("SELECT * FROM pg_listings")
        listings = cur.fetchall()
        cur.close()
        conn.close()

        data_structure = minheap.MinHeap()

        # Get lat, lon of college
        college_lat, college_lon = college_address[0],college_address[1]
        print(college_lat,college_lon)

        # Process listings
        for listing in listings:
            node = minheap.Node(listing[0], listing[1], listing[2], listing[3], listing[4],
                                listing[5], listing[6], listing[7], listing[8], listing[9],
                                listing[10], listing[11], listing[12],listing[13], listing[14])
            node.distance = node.calculate_distance(college_lat,college_lon,listing[13],listing[14]) # Set distance
            data_structure.push(node)

        print(data_structure)

        return jsonify({"listings": listings}), 200

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return jsonify({"error": "Failed to retrieve listings"}), 500


@app.route('/get_address', methods=['GET'])
def get_address():
    return jsonify({"college_address": college_address})


if __name__ == '__main__':
    app.run(debug=False)
