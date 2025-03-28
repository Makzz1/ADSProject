from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file
DATABASE_URL = os.getenv("DATABASE_URL")

print("Database URL:", DATABASE_URL)
print("EMAIL_USER:", os.getenv("EMAIL_USER"))
print("EMAIL_PASSWORD:", os.getenv("EMAIL_PASSWORD"))
