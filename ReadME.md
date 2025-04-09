# 💸 Django Finance Tracker

A powerful and user-friendly personal finance tracker built with Django. Users can register, log in, manage transactions (income and expenses), create custom categories, view insightful dashboards, and export reports in CSV or PDF formats.

---

## 🚀 Features

### 👤 User Authentication
- Secure registration and login system.
- Profile view and editable user profile.

### 💰 Transaction Management
- Add, edit, delete transactions.
- Supports both income and expense types.
- Filter by date range, category, and amount.

### 📊 Dashboard Insights
- Monthly income, expenses, and balance summary.
- Visual charts for spending by category and savings over time.

### 📁 Report Generation
- Export monthly reports in **CSV** or **PDF** format.

### 🗂️ Category Management
- Custom categories for income and expenses.
- Create, update, or delete categories.

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default), can be configured to PostgreSQL/MySQL
- **Charting:** Chart.js (for dashboard visuals)
- **PDF Export:** ReportLab
- **CSV Export:** Python `csv` module

---

## 📂 Project Structure

```plaintext
finance_tracker/
├── templates/                # HTML templates
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   └── ...
├── static/                   # Static files (CSS/JS)
├── models.py                 # Transaction & Category models
├── views.py                  # All main app logic
├── forms.py                  # Django forms (Register, Transaction, Category)
├── urls.py                   # App routes
├── admin.py                  # Django admin config
└── ...
```

---

## 🧪 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/finance-tracker.git
cd finance-tracker
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to start tracking your finances!

---

## 📦 Export Reports

Navigate to the **Report** page on the dashboard and select a month:
- Export as **CSV**
- Export as **PDF**

---

## 🔒 Admin Access

To create an admin user:

```bash
python manage.py createsuperuser
```

Login at `/admin` to manage users, transactions, and categories.

---

## 🤝 Contributions

Contributions are welcome!  
Fork the repo and submit a PR with your improvements.

---

## 📜 License

Licensed under the [MIT License](LICENSE).

---

## 📬 Contact Me

Feel free to reach out for any questions or suggestions:  

- **GitHub**: [obaidullah72](https://github.com/obaidullah72)  
- **LinkedIn**: [obaidullah72](https://www.linkedin.com/in/obaidullah72/)  

[![Visitor Count](https://visitcount.itsvg.in/api?id=obaidullah72&label=Profile%20Views&color=0&icon=0&pretty=true)](https://visitcount.itsvg.in)
