# FoodSaver v2

FoodSaver is a web application designed to bridge the gap between food surplus and hunger. It connects food donors (restaurants, hotels, individuals) with NGOs and claimants to ensure excess food reaches those in need efficiently.

## Features
*   **Donor Dashboard**: Post food listings, manage surplus, and track claim history.
*   **Claimant Dashboard**: Browse available food, view maps, and claim donations.
*   **AI Analytics**: Usage of Google Gemini AI for food waste reduction insights.
*   **Leaderboard**: Track top donors and community impact.

---

## Prerequisites
*   Python 3.10 or higher
*   Git

## Installation & Setup

Follow these steps to set up the project on a new machine.

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd "Foodsaver v2"
```

### 2. Create a Virtual Environment
It is recommended to use a virtual environment to manage dependencies.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Initialize the database and apply migrations.
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)
To access the Django Admin panel:
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```
The application will be available at `http://127.0.0.1:8000/`.

---

## Usage

### User Roles
*   **Donor**: Can create food listings.
*   **Claimant (NGO/Individual)**: Can search and claim listings.

### First Time Login
If the database was reset, you will need to register a new account on the **Join Us** page.

---

## Troubleshooting
*   **ModuleNotFoundError**: Ensure your virtual environment is activated and you have installed requirements (`pip install -r requirements.txt`).
*   **Database Errors**: Run `python manage.py migrate` to ensure the database schema is up to date.
