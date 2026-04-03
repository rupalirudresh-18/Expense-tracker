# 💰 Expense Tracker

A full-stack **Expense Tracker Web Application** built using **FastAPI (backend)** and **HTML, CSS, JavaScript (frontend)**. 
This application helps users manage their daily expenses efficiently with authentication and complete CRUD operations.

## 🚀 Features

- 🔐 Secure User Authentication (JWT-based Login & Signup)
- ➕ Add Expenses with category & description
- 📋 View all user-specific expenses
- 🔍 Filter expenses by category
- ✏️ Update existing expenses
- ❌ Delete expenses

## 🛠️ Tech Stack

### Backend 
- FastAPI
- SQLite (Database)
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- JWT Authentication

### Frontend
- HTML
- CSS3 (Glassmorphism UI)
- JavaScript (Fetch API)

## 📁 Project Structure

```
Expense-tracker/
│
├── frontend/
│   └── index.html
│
├── main.py
├── models.py
├── database.py
├── expenses.db
└── README.md
```


## ⚙️ How to Run Locally

### 1. Clone the repository
```
git clone https://github.com/your-username/Expense-tracker.git
cd Expense-tracker
```

### 2. Install dependencies
```
pip install fastapi uvicorn
```

### 3. Run backend server
```
uvicorn main:app --reload
```

### 4. Open frontend
- Open `frontend/index.html` in your browser  
OR  
- Use Live Server in VS Code  

---

## 🌐 API Access

- Base URL:  
```
http://127.0.0.1:8000
```

- Swagger UI:  
```
http://127.0.0.1:8000/docs
```


## 📸 Screenshots

(Add your screenshots here)

```
![Login Page](images/login.png)
![Dashboard](images/dashboard.png)
![Add Expense](images/add.png)
```

---

## 💡 Future Improvements

- Add charts and analytics
- Deploy backend (Render / Railway)
- Deploy frontend (GitHub Pages)
- Add notifications

---

## 🙌 Author

Rupali R  
Computer Science & Engineering Student  

---

## 🌟 Key Highlights

- Full-stack application with frontend-backend integration
- Token-based authentication using JWT
- RESTful API design using FastAPI
- Clean and responsive glassmorphism UI
- State-managed frontend (no unnecessary page reloads)
