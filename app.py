from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import psycopg2
from backend import minheap
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

app = Flask(__name__)
app.secret_key = '1234'  # Required for session management
CORS(app)

# Global variable to store the address
college_lat = None
college_lon = None

# Database connection details
load_dotenv()

# Database connection details (Now from environment variables)
DB_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'sslmode': 'require'
}


def connect_db():
    """Connect to the PostgreSQL database."""
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('preferences.html')

@app.route('/manager_verification', methods=['GET', 'POST'])
def manager_verification():
    if request.method == 'POST':
        if 'secret_code' not in session:
            # First submission - collect details and send verification code
            name = request.form.get('name')
            email = request.form.get('email')
            contact = request.form.get('contact')
            id_type = request.form.get('verification_type')
            id_number = request.form.get('id_number')
            
            # Generate and store secret code
            secret_code = generate_secret_code()
            print(f"Generated secret code: {secret_code}")  # Debug log
            session['secret_code'] = secret_code
            session['manager_details'] = {
                'name': name,
                'email': email,
                'contact': contact,
                'id_type': id_type,
                'id_number': id_number
            }
            
            # Send verification email
            if send_verification_email(email, name, secret_code):
                return render_template('verify_code.html', email=email)
            else:
                return "Failed to send verification email. Please check the email address and try again.", 500
        else:
            # Second submission - verify the code
            submitted_code = request.form.get('verification_code', '').strip().upper()
            stored_code = session.get('secret_code', '').strip().upper()
            
            print(f"Submitted code: {submitted_code}")  # Debug log
            print(f"Stored code: {stored_code}")  # Debug log
            
            if submitted_code and submitted_code == stored_code:
                # Store verification status in session
                session['manager_verified'] = True
                # Clear sensitive data
                session.pop('secret_code', None)
                return redirect(url_for('manager_page'))
            else:
                return render_template('verify_code.html', 
                                    error="Invalid verification code. Please try again.",
                                    email=session['manager_details']['email'])
                
    return render_template('manager_verification.html')

@app.route('/manager_page')
def manager_page():
    if not session.get('manager_verified'):
        return redirect(url_for('manager_verification'))
    return render_template('manager_page.html')

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

@app.route('/submit_pg', methods=['POST'])
def submit_pg():
    if not session.get('manager_verified'):
        return redirect(url_for('manager_verification'))
    
    try:
        # Get form data with validation
        name = request.form.get('name').strip()
        if not name:
            raise ValueError("PG Name is required")

        try:
            price = float(request.form.get('price', 0))
            deposit = float(request.form.get('deposit', 0))
            bedrooms = int(request.form.get('bedrooms', 0))
            if price < 0 or deposit < 0 or bedrooms < 1:
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Invalid price, deposit, or bedroom values")

        ac_non_ac = request.form.get('ac_non_ac')
        if ac_non_ac not in ['AC', 'Non-AC', 'Both']:
            raise ValueError("Invalid AC/Non-AC option")

        gender = request.form.get('gender')
        if gender not in ['Male', 'Female', 'Any']:
            raise ValueError("Invalid gender option")

        address = request.form.get('address').strip()
        if not address:
            raise ValueError("Address is required")

        try:
            latitude = float(request.form.get('latitude', 0))
            longitude = float(request.form.get('longitude', 0))
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("Invalid latitude or longitude values")

        contact = request.form.get('contact', '').strip()
        if not contact.isdigit() or len(contact) != 10:
            raise ValueError("Invalid contact number")

        # Get amenities (checkboxes)
        wifi = 'wifi' in request.form
        fridge = 'fridge' in request.form
        oven = 'oven' in request.form
        washing_machine = 'washing_machine' in request.form
        furnished = 'furnished' in request.form
        parking = 'parking' in request.form

        # Connect to database
        conn = connect_db()
        cur = conn.cursor()

        # Insert into database
        cur.execute('''
            INSERT INTO pg_listings (
                "Name", price, bedrooms, "AC_NON_AC", deposit, "Gender",
                address, latitude, longitude, contact,
                wifi, fridge, oven, washing_machine, furnished, "Parking"
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''', (
            name, price, bedrooms, ac_non_ac, deposit, gender,
            address, latitude, longitude, contact,
            wifi, fridge, oven, washing_machine, furnished, parking
        ))

        # Commit the transaction
        conn.commit()
        cur.close()
        conn.close()

        # Return success message with cleared form
        return render_template('manager_page.html', 
                             success_message=f"PG listing '{name}' has been added successfully!")

    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        return render_template('manager_page.html', error_message=str(ve))
    except Exception as e:
        print(f"Error adding PG listing: {e}")
        return render_template('manager_page.html', 
                             error_message="Failed to add PG listing. Please check your input and try again.")

def generate_secret_code(length=6):
    """Generate a random secret code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def send_verification_email(recipient_email, name, secret_code):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASSWORD")
    subject = "Nammastay - Manager Account Verification"
    
    body = f'''Dear {name},

Welcome to Nammastay! We're excited to have you as a potential manager on our platform.

Your verification code is: {secret_code}

Please use this code to complete your account verification process. For security reasons, this code is valid only for this session.

Important:
- This code is required to access the manager dashboard
- Do not share this code with anyone
- The code is valid only for this session

If you did not request this verification, please ignore this email.

Best regards,
The Nammastay Team
    '''
    
    try:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f'Failed to send email. Error: {e}')
        return False

if __name__ == '__main__':
    app.run()
