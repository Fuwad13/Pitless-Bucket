from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User

DATABASE_URL = 'sqlite:///test.db'

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind = engine)
session = SessionLocal()

# Create a new user
new_user = User(name="John Doe", email="johndoe@example.com", password_hash="hashedpassword")
session.add(new_user)
session.commit()
print(f"User {new_user.name} added with ID {new_user.id}")
users = session.query(User).all()
for user in users:
    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
