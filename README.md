# 📚 Online Book Store

A Django-based **Online Book Store web application** that allows users to browse books, search for products, manage their profiles, and interact with an online shopping system. The project also includes an admin panel for managing books, users, and store-related data.

The application was developed as a practical full-stack web project using **Python and Django**, with a focus on database-driven functionality, user management, product handling, and e-commerce workflows.

---

## 🚀 Project Overview

The Online Book Store provides a simple platform where users can:

* Browse available books
* Search for books
* View book details
* Manage their user profile
* Interact with the shopping workflow
* Use authentication-based features

Administrators can manage books and application data through the Django admin panel.

The project currently contains **100+ book records** for testing and demonstration.

---

## 🛠️ Technologies Used

### Backend

* **Python**
* **Django 5.2.4**
* Django ORM
* Django Authentication
* SQLite

### Frontend

* HTML5
* CSS3
* Bootstrap
* JavaScript
* AJAX
* Django Templates

### APIs & Payments

* Stripe API
* Email SMTP integration

### Development Tools

* Git
* GitHub
* VS Code

### Python Libraries

* Django
* Pillow
* Requests
* Stripe

---

## ✨ Key Features

### 👤 User Features

* User registration and authentication
* User profile management
* Book browsing
* Book search
* Book details
* Image-based profile functionality

### 📖 Book Management

* Book listing
* Book details
* Book cover images
* Database-driven book records
* Admin-side book management

### 💳 Payment Integration

* Stripe payment integration
* Secure payment workflow using Stripe API

### 📧 Email Integration

* SMTP-based email functionality
* Gmail SMTP configuration

### 🔐 Admin Panel

Django's built-in admin panel is used to manage application data and book records.

---

## 📁 Project Structure

```text
Online-Book-Store/
│
├── adminapp/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── mainapp/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── userapp/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── obsproject/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ How to Run the Project Locally

Follow the steps below to set up the project on your computer.

## 1. Clone the Repository

```bash
git clone https://github.com/AmanGupta0998/Online-Book-Store.git
```

Go into the project directory:

```bash
cd Online-Book-Store
```

---

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

### Windows

Activate it using:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the main dependencies manually:

```bash
pip install django pillow requests stripe
```

---

## 4. Configure Environment Variables

The project uses environment variables for sensitive credentials such as:

* Django Secret Key
* Stripe Secret Key
* Email credentials

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your_django_secret_key
STRIPE_SECRET_KEY=your_stripe_secret_key
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

> ⚠️ Never upload the `.env` file to GitHub.

The `.env` file is excluded through `.gitignore`.

---

## 5. Apply Database Migrations

Run:

```bash
python manage.py makemigrations
```

Then:

```bash
python manage.py migrate
```

This will create/update the local SQLite database.

---

## 6. Create an Admin User

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

Enter the requested:

* Username
* Email
* Password

---

## 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see something similar to:

```text
Starting development server at http://127.0.0.1:8000/
```

Open the following address in your browser:

```text
http://127.0.0.1:8000/
```

For the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

# 🔑 Environment Variables

| Variable              | Purpose                     |
| --------------------- | --------------------------- |
| `DJANGO_SECRET_KEY`   | Django application security |
| `STRIPE_SECRET_KEY`   | Stripe payment integration  |
| `EMAIL_HOST_USER`     | SMTP email account          |
| `EMAIL_HOST_PASSWORD` | SMTP authentication         |

Make sure these values are configured before running features that depend on Stripe or email services.

---

# 🖼️ Media & Images

The project uses Django's media configuration for uploaded images such as:

* Book cover images
* User profile images

Django's `ImageField` requires the **Pillow** package.

Install Pillow if required:

```bash
pip install pillow
```

---

# 🔒 Security

Sensitive credentials are stored using environment variables instead of being hardcoded in the source code.

The following files/data should not be committed:

```text
.env
db.sqlite3
media/
venv/
__pycache__/
```

---

# 📌 Important Notes

* This project is configured for local development.
* SQLite is used as the development database.
* Stripe requires valid API credentials for payment functionality.
* Gmail SMTP requires appropriate email credentials/app password.
* `DEBUG = True` is intended for development and should be disabled in production.
* Additional production configuration is required before deployment.

---

# 🎯 Purpose of the Project

This project was developed to gain practical experience in:

* Django web development
* Full-stack application development
* Database management
* Django ORM
* Authentication
* REST/API integration
* Payment gateway integration
* Email integration
* Image handling
* Git and GitHub workflow

---

## 👨‍💻 Developer

**Aman Gupta**

B.Tech CSE (AI & ML)

GitHub:
https://github.com/AmanGupta0998

---

⭐ If you find this project useful, feel free to explore the repository and its implementation.
