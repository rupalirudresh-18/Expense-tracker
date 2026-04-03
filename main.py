from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= SECURITY =================
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ================= DATABASE =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= AUTH HELPERS =================
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        token = credentials.credentials   # ✅ IMPORTANT FIX
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(models.User).filter(models.User.username == username).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ================= USER APIs =================

@app.post("/signup")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = hash_password(password)

    new_user = models.User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ================= EXPENSE APIs =================

# ➕ ADD
@app.post("/add-expense")
def add_expense(
    amount: float,
    category: str,
    description: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_expense = models.Expense(
        amount=amount,
        category=category,
        description=description,
        user_id=user.id
    )

    db.add(new_expense)
    db.commit()

    return {"message": "Expense added successfully"}


# 📄 GET (with filters)
@app.get("/expenses")
def get_expenses(
    category: str = None,
    min_amount: float = None,
    max_amount: float = None,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(models.Expense).filter(models.Expense.user_id == user.id)

    if category:
        query = query.filter(models.Expense.category == category)

    if min_amount:
        query = query.filter(models.Expense.amount >= min_amount)

    if max_amount:
        query = query.filter(models.Expense.amount <= max_amount)

    expenses = query.all()

    return {
        "expenses": [
            {
                "id": exp.id,
                "amount": exp.amount,
                "category": exp.category,
                "description": exp.description
            }
            for exp in expenses
        ]
    }


# ❌ DELETE
@app.delete("/delete-expense/{id}")
def delete_expense(
    id: int,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == id,
        models.Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Deleted successfully"}


# ✏️ UPDATE
@app.put("/update-expense/{id}")
def update_expense(
    id: int,
    amount: float,
    category: str,
    description: str,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    expense = db.query(models.Expense).filter(
        models.Expense.id == id,
        models.Expense.user_id == user.id
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = amount
    expense.category = category
    expense.description = description

    db.commit()

    return {"message": "Updated successfully"}