from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "mysql+mysqlconnector://root:Chabi@1998@127.0.0.1:3306/Fast_api"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True for logging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def check_db_connection():
    # Use a context manager to ensure the session is properly closed
    with SessionLocal() as session:
        try:
            # Use text() to specify the SQL statement as a text object
            session.execute(text("SELECT 1"))
            print("Connection successful")
        except Exception as e:
            print(f"Connection failed: {e}")

# Call the function to check the connection
if __name__ == "__main__":
    check_db_connection()
