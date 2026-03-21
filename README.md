# HRMS Lite - Backend

HRMS Lite Backend is a robust, highly scalable REST API service for managing core Human Resource operations. Built on **Django** and **Django REST Framework (DRF)**, it uses Class-Based Views (CBVs) to handle business logic, data validation, metrics reporting, and secure database interactions seamlessly.

---

## 🚀 Features

- **RESTful API Architecture:** Standardized predictable API endpoints for all entities.
- **Employee & Department Management:** Full CRUD capabilities with support for soft and hard deletes.
- **Attendance Processing:** Check-in APIs, status tracking, and automated validation.
- **Analytics & Reporting:** High-performance dashboard endpoints aggregating real-time corporate metrics.
- **Secure Configuration:** Application secrets decoupled from source code using `python-decouple`.
- **Database Ready:** Pre-configured to support PostgreSQL via `psycopg2-binary`.

---

## 🛠️ Technology Stack

- **Framework:** [Django (v4.2)](https://www.djangoproject.com/)
- **API Engine:** [Django REST Framework](https://www.django-rest-framework.org/)
- **Database Toolkit:** PostgreSQL (`psycopg2-binary`)
- **Environment Management:** [python-decouple](https://pypi.org/project/python-decouple/)
- **CORS Handling:** `django-cors-headers`

---

## 📂 Project Structure

```
quesscorp-hrms-backend/
├── api/                  # Django REST framework viewsets, routers, and serializers
├── config/               # Project-level configuration (settings.py, urls.py, wsgi/asgi)
├── Schema/               # Core data models, migrations, and database schema definitions
├── utilities/            # Helper scripts, common functions, and middleware
├── manage.py             # Django execution script
├── requirements.txt      # Python dependencies block
├── uv.lock               # UV precise dependency lockfile
└── .env                  # Environment variables
```

---

## ⚙️ Setup & Installation

To run this project locally, ensure you have Python 3.8+ installed along with `pip` and optionally `uv`.

### 1. Clone & Enter Directory
```bash
cd hrms_lite/quesscorp-hrms-backend
```

### 2. Set Up Virtual Environment
Create and activate your Python virtual environment to isolate project dependencies.
```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file based on your local settings. At a minimum, define your Django SECRET_KEY and Database credentials.
```env
SECRET_KEY=your_secure_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
# Update DB credentials depending on your PostgreSQL setup
DATABASE_URL=postgres://user:password@localhost:5432/hrms_db
```

### 5. Apply Database Migrations
Initialize your database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)
To access the built-in Django admin interface at `/admin`, create an admin account:
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The backend API will now be accessible at `http://127.0.0.1:8000`.

---

## 🤝 Best Practices Observed
- **Class-Based Views (CBVs):** Enforces DRY (Don't Repeat Yourself) principles and code reusability.
- **Dependency Isolation:** Strict environment bounds via `requirements.txt` and `.env`.
- **CORS Security:** Secured requests from diverse frontend domains using `django-cors-headers`.
