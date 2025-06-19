<h1 align="center">🏠 Hostel Accommodation Portal - Chennai Students</h1>

<p align="center">
  A student-friendly web app to search and manage hostel stays in Chennai.
  <br />
  <i>Built with Flask and PostgreSQL</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Backend-blue" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-blueviolet" />
  <img src="https://img.shields.io/badge/Made%20with-%F0%9F%92%BB%20Love-red" />
</p>

---

## 📚 Overview

This project is a hostel booking platform tailored for college students in Chennai. Users can browse hostels and view details. Hostel owners can manage listings, and admins have platform-wide control.

---

## ⚙️ Tech Stack

<div align="center">

| Layer       | Technology          |
|-------------|---------------------|
| Backend     | 🐍 Flask            |
| Database    | 🐘 PostgreSQL       |
| Frontend    | 🌐 HTML, CSS        |
| Deployment  | 🚀 Render           |

</div>

---

## 🛠️ Features

✅ Student Sign-up/Login  
✅ Hostel listing with filters  
✅ Owner dashboard to manage properties  
✅ Admin panel for moderation  
✅ Secure password handling (bcrypt)  
✅ Mobile-friendly responsive UI  

---

## 🔁 Workflow

- [ ] Design DB schema (Users, Hostels, Bookings...)
- [ ] Build Flask routes and templates
- [ ] Implement user authentication
- [ ] Add hostel listing & booking modules
- [ ] Integrate PostgreSQL
- [ ] Develop owner and admin dashboards
- [ ] Test and deploy

---

## 📷 Screenshots

<h3>🏡 Home Page</h3>

![image](https://github.com/user-attachments/assets/e137760c-0322-47cb-9de9-bc94a4e9644f)

<h3>📋 Hostel Available Page</h3>

![image](https://github.com/user-attachments/assets/a1dd2ec7-7c37-4598-8719-7d771fa4217b)

<h3>ℹ️ Hostel Info Page</h3>

![image](https://github.com/user-attachments/assets/7cea254b-e04f-4a7c-9e1a-614013e03ea8)

<h3>ℹ️ Admin Side-Manager Verification </h3>

![image](https://github.com/user-attachments/assets/b8eb79a5-386b-4871-91ea-9e4ef4cdb9b5)

<h3>🏠 Admin page-Adding new hostel </h3>

![image](https://github.com/user-attachments/assets/262e13e0-6cab-4d8a-bf27-5f6f2c995a84)

---

## 💻 Local Setup Instructions

Follow these steps to set up the project locally:

```bash

# 1. Clone the repository
git clone https://github.com/your-username/hostel-accommodation.git
cd hostel-accommodation

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install required packages
pip install -r requirements.txt

# 4. Set up the PostgreSQL database
# Ensure PostgreSQL is installed and running, then create your DB
# Example (psql): CREATE DATABASE hostel_db;

# 5. Configure your environment variables in a `.env` file
# Example:
# DATABASE_URL=postgresql://username:password@localhost/hostel_db

# 6. Run the application
flask run

```

🙋 Contact
Made with ❤️ by Maghizh
📧 maghizhvanban.com
