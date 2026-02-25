📝 ThoughtHub – Django Blog Platform
# ThoughtHub 📝

ThoughtHub is a Django-based blogging platform that allows users to explore blog posts across multiple categories.  
It includes a custom admin dashboard for managing posts and categories.

🌐 **Live Demo:**  
👉 https://thoughthub-sj98.onrender.com/

---

## 🚀 Features

- 🏠 Homepage with latest blog posts
- 🔎 Search functionality
- 🗂️ Category-based filtering
- 📝 Post detail page
- 🔐 Admin dashboard for managing content
- 🏷️ Slug-based URLs (SEO friendly)
- 📱 Responsive design
- 🌍 Deployed on Render

---

## 🛠️ Tech Stack

- **Backend:** Python, Django 5
- **Frontend:** HTML5, CSS3
- **Database:** SQLite (Development)
- **Deployment:** Render
- **Production Server:** Gunicorn
- **Static File Handling:** Whitenoise

---

## 📂 Project Structure


thoughthub/
│── blog/
│── blogwebsite/
│── templates/
│── static/
│── media/
│── manage.py
│── requirements.txt
│── db.sqlite3


---

## ⚙️ Local Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Sanjeet0007/thoughthub.git
cd thoughthub
2️⃣ Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
4️⃣ Apply migrations
python manage.py migrate
5️⃣ Create superuser
python manage.py createsuperuser
6️⃣ Run development server
python manage.py runserver

Visit:

http://127.0.0.1:8000/

Admin panel:

http://127.0.0.1:8000/admin/
🌍 Deployment

This project is deployed on Render using:

Gunicorn as WSGI server

Environment variables for secure configuration

Whitenoise for static file serving
