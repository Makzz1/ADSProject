from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
import psycopg2
import minheap

app = Flask(__name__)
CORS(app)

# Global variable to store the address
college_lat = None
college_lon = None

# Database connection details
DB_CONFIG = {
    'dbname': "postgres",
    'user': "postgres.nbwcvxybhyhtjzcyxjmn",
    'password': "1@Maghizh",
    'host': "aws-0-ap-south-1.pooler.supabase.com",
    'port': "6543"
}

def connect_db():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)
@app.route('/')
def home():
    return render_template('preferences.html')

@app.route('/second_page')
def second_page():
    return render_template('second_page.html')

@app.route('/third_page')
def third_page():
    return render_template('third_page.html')

@app.route('/save_address', methods=['POST'])
def save_address():
    

    global college_lat, college_lon, selected_college_name
    data = request.json
    address = data.get("address")
    college_name = data.get("name")

    if address and isinstance(address, list) and len(address) == 2:
        college_lat, college_lon = address
        selected_college_name = college_name
        print(f" Received Address (Lat, Lon): {college_lat}, {college_lon} for {selected_college_name}")
    else:
        return jsonify({"error": "Invalid address format"}), 400

    return jsonify({"message": "Address saved successfully"}), 200

@app.route('/get_pg_listings', methods=['GET'])
def get_pg_listings():
    """Fetch PG listings and return with selected college details."""
    global college_lat, college_lon

    if college_lat is None or college_lon is None:
        return jsonify({"error": "College address not found"}), 400

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Fetch PG listings
        cur.execute('''
            SELECT "Name", price, address, wifi, bedrooms, deposit, "AC_NON_AC", 
                   "Parking", fridge, washing_machine, oven, furnished, "Gender", 
                   latitude, longitude FROM pg_listings;
        ''')
        listings = cur.fetchall()

        cur.execute("SELECT MIN(price), MAX(price) FROM pg_listings;")
        min_price, max_price = cur.fetchone()

        cur.close()
        conn.close()

        if not listings:
            return jsonify({"error": "No PG listings found"}), 404

        data_structure = minheap.MinHeap()

        formatted_listings = []
        for listing in listings:
            name, price, address, wifi, bedrooms, deposit, ac, parking, fridge, washing_machine, oven, furnished, gender, lat, lon = listing
            node = minheap.Node(price, name, address, wifi, bedrooms, deposit, ac, parking, fridge, washing_machine, oven, furnished, gender, lat, lon)
            node.distance = minheap.Node.calculate_distance(college_lat, college_lon, lat, lon)

            data_structure.push(node)

            def format_amenities(wifi, ac, parking, fridge, washing_machine, oven, furnished):
                """Convert boolean values to readable amenities list."""
                amenities = []
                if wifi: amenities.append("WiFi")
                if ac: amenities.append("AC")
                if parking: amenities.append("Parking")
                if fridge: amenities.append("Fridge")
                if washing_machine: amenities.append("Washing Machine")
                if oven: amenities.append("Oven")
                if furnished: amenities.append("Furnished")
                return ", ".join(amenities) if amenities else "No amenities"

            formatted_listings.append({
                "name": name,
                "price": price,
                "distance": round(node.distance, 2),
                "address": address,
                "amenities": format_amenities(wifi, ac, parking, fridge, washing_machine, oven, furnished),
                "gender": gender,
                "latitude": lat,
                "longitude": lon
            })

        return jsonify({
            "college_name": selected_college_name,
            "college_lat": college_lat,
            "college_lon": college_lon,
            "min_price": min_price,
            "max_price": max_price,
            "listings": formatted_listings
        }), 200

    except Exception as e:
        print("Error fetching PG listings:", e)
        return jsonify({"error": "Failed to fetch PG listings"}), 500

@app.route('/get_pg_details', methods=['GET'])
def get_pg_details():
    """Fetch details for a specific PG listing."""
    pg_id = request.args.get('id')
    
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Fetch the specific PG listing
        cur.execute('''
            SELECT "Name", price, address, wifi, bedrooms, deposit, "AC_NON_AC", 
                   "Parking", fridge, washing_machine, oven, furnished, "Gender", 
                   latitude, longitude 
            FROM pg_listings 
            WHERE "Name" = %s;
        ''', (pg_id,))
        
        listing = cur.fetchone()
        cur.close()
        conn.close()

        if not listing:
            return jsonify({"error": "PG not found"}), 404

        name, price, address, wifi, bedrooms, deposit, ac, parking, fridge, washing_machine, oven, furnished, gender, lat, lon = listing
        
        # Calculate distance from college
        distance = minheap.Node.calculate_distance(college_lat, college_lon, lat, lon)

        def format_amenities(wifi, ac, parking, fridge, washing_machine, oven, furnished):
            """Convert boolean values to readable amenities list."""
            amenities = []
            if wifi: amenities.append("WiFi")
            if ac: amenities.append("AC")
            if parking: amenities.append("Parking")
            if fridge: amenities.append("Fridge")
            if washing_machine: amenities.append("Washing Machine")
            if oven: amenities.append("Oven")
            if furnished: amenities.append("Furnished")
            return ", ".join(amenities) if amenities else "No amenities"

        return jsonify({
            "name": name,
            "price": price,
            "distance": round(distance, 2),
            "address": address,
            "amenities": format_amenities(wifi, ac, parking, fridge, washing_machine, oven, furnished),
            "gender": gender,
            "latitude": lat,
            "longitude": lon
        }), 200

    except Exception as e:
        print("Error fetching PG details:", e)
        return jsonify({"error": "Failed to fetch PG details"}), 500

if __name__ == '__main__':
    app.run(debug=True)
