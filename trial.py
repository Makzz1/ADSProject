import pandas as pd
from supabase import create_client, Client

# Supabase credentials (Replace with your actual Supabase URL and API key)
SUPABASE_URL = "https://nbwcvxybhyhtjzcyxjmn.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5id2N2eHliaHlodGp6Y3l4am1uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgyMTA5MzYsImV4cCI6MjA1Mzc4NjkzNn0.XObIBTSmKIMGswm72rdvdfDuqG3Nozgdjhky8bsoLX4"  # Replace with your Supabase API key


# Connect to Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Load CSV file
file_path = "D:/downloads/archive (1)/accommodation.csv"  # Update with correct file path
df = pd.read_csv(file_path)

# 🔹 **Ensure modifications happen on the original DataFrame**
df = df.copy()

# 🔹 **Fix NaN values & enforce correct types**
for col in df.columns:
    if df[col].dtype == 'float64':
        df[col] = df[col].fillna(0)  # Replace NaN in float columns with 0.0
    elif df[col].dtype == 'object':
        df[col] = df[col].fillna("").astype(str)  # Replace NaN in string columns with ""

# 🔹 **Convert boolean-like object columns to proper boolean values (Yes/No → True/False)**
boolean_cols = ['Gas', 'Electricity', 'Water', 'Internet', 'Fridge', 'Freezer', 'Oven', 'Microwave',
                'Dishwasher', 'Washing machine', 'Dryer', 'Furnished', 'Double glazing',
                'Separate lounge', 'Bath', 'Shower', 'Alarm', 'Fire alarm', 'Garden',
                'Off road parking', 'Garage', 'Wifi', 'Sky/Cable package',
                'Energy performance certificate', 'Gas safe registered',
                'Electrical safety certificate', 'NRLA registered']

for col in boolean_cols:
    if col in df.columns:
        df[col] = df[col].map(lambda x: True if str(x).strip().lower() == 'yes' else False)

# 🔹 **Ensure JSON Compliance**
df = df.astype(object)  # Convert all columns to generic object dtype for JSON compatibility

# 🔹 **Print Debug Info**
print("🔍 Data Preview:\n", df.head())
print("📊 Column Data Types:\n", df.dtypes)

# Convert DataFrame to list of dictionaries
data_list = df.to_dict(orient="records")

# Insert data into Supabase table
TABLE_NAME = "pg_listings"  # Replace with your actual table name

try:
    response = supabase.table(TABLE_NAME).insert(data_list).execute()
    print("✅ Data uploaded successfully:", response)
except Exception as e:
    print("❌ Error inserting data:", e)


response = supabase.table("pg_listings").select("*").execute()
print("📊 Retrieved Data from Supabase:", response.data)

