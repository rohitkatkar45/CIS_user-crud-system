# 🛠️ User CRUD System with RBAC, JWT, Task Management, and Auto-Deactivation

## 📌 Project Overview

This project is a **User and Task Management System** built with **Django** and **DRF**, providing:
- Role-Based Access Control (**RBAC**) for `Admin`, `Manager`, and `User`
- **JWT Authentication**
- Task creation with **deadlines**
- **Missed task detection** and **automatic user deactivation**
- **Reactivation** logic by the Manager

---

## 🧩 Features

### 🔐 Authentication
- Secure user registration and login with **JWT**
- Password validation and confirmation
- Token refresh and logout functionality

### 👥 User Roles
- `ADMIN`: Full control (Users & Tasks)
- `MANAGER`: Create/update users & assign tasks
- `USER`: View and complete assigned tasks

### ✅ Task Management
- Managers assign tasks to users with deadlines
- Users update their task status (`Pending`, `Completed`)
- Deadline checker marks tasks as `Missed`
- If 5 or more deadlines missed in a week → **Auto Deactivation**
- Managers can **reactivate** users

### 🔔 Notifications
- Console notifications for each missed deadline
- Missed tasks tracked weekly

---

## 🧰 Tech Stack

- **Backend**: Python, Django, Django Rest Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **Environment**: `.env` support for DB and secret management
- **Containerization** (Optional): Docker + Docker Compose

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL
- pip & virtualenv

### Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/rohitkatkar45/CIS_user-crud-system.git
cd CIS_user-crud-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # For Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env with DB credentials and secret key

# 5. Migrate and create superuser
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
