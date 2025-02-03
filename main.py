from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('D:/pycharm/ADS Project/data.env')

# Access the variables
database_url = os.getenv('DATABASE_URL')
api_key = os.getenv('API_KEY')

print(database_url)
print(api_key)

