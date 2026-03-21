from getpass import getpass
from sqlmodel import Session, select
from db import engine
from models import User
from auth import get_password_hash, create_access_token
from datetime import timedelta

def create_admin_user():
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        existing = session.exec(statement).first()
        if existing:
            print("User already exists.")
            if not existing.is_admin:
                existing.is_admin = True
                session.add(existing)
                session.commit()
                print("User promoted to admin.")
        else:
            user = User(
                username=username,
                hashed_password=get_password_hash(password),
                is_admin=True,
            )
            session.add(user)
            session.commit()
            print("Admin user created.")

def get_admin_token():
    username = input("Enter admin username: ")
    with Session(engine) as session:
        statement = select(User).where(User.username == username, User.is_admin == True)
        user = session.exec(statement).first()
        if not user:
            print("Admin user not found.")
            return

        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=60 * 24 * 365), # 1 year
        )
        print(f"Your admin token:
{access_token}")


if __name__ == "__main__":
    print("1. Create admin user")
    print("2. Get admin token")
    choice = input("Choose an option: ")
    if choice == "1":
        create_admin_user()
    elif choice == "2":
        get_admin_token()
    else:
        print("Invalid option.")
