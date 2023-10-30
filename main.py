from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine,Base
from models import Base
from models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

class User(BaseModel):
    # id: int
    username: str
    password: str

# Initialize FastAPI
app = FastAPI()

# Task 1: CRUD APIs Development
def get_db():
    print("fastapi")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def read_root():
    return {"Hello": "World"}        

# Create User
@app.post("/users", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get User by ID
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update User
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete User
@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return

# Task 2: Implement OAuth2 for Login

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token route
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authentication logic here
    # Return the token
    pass

# Task 3: Database Migration with Alembic

# (Alembic migrations will be generated based on the model in models.py)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


    
