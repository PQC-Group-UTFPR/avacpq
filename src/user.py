import sqlite3
from flask_login import UserMixin
from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        """Search for a user by ID"""
        db = None
        try:
            db = get_db()
            user = db.execute(
                "SELECT * FROM user WHERE id = ?", (user_id,)
            ).fetchone()
            
            if not user:
                return None

            user = User(
                id_=user['id'], 
                name=user['name'], 
                email=user['email'], 
                profile_pic=user['profile_pic']
            )
            return user
        except sqlite3.Error as e:
            print(f"Error fetching user by ID: {e}")
            return None
        finally:
            if db:
                db.close()

    @staticmethod
    def create(id_, name, email, profile_pic):
        """Create a new user in the database"""
        db = None
        try:
            db = get_db()
            db.execute(
                "INSERT INTO user (id, name, email, profile_pic) "
                "VALUES (?, ?, ?, ?)",
                (id_, name, email, profile_pic),
            )
            db.commit()
            print(f"User {name} created successfully.")
            return True
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            if db:
                db.close()

    @staticmethod
    def get_by_email(email):
        """Search for a user by email"""
        db = None
        try:
            db = get_db()
            user = db.execute(
                "SELECT * FROM user WHERE email = ?", (email,)
            ).fetchone()
            
            if not user:
                return None

            user = User(
                id_=user['id'], 
                name=user['name'], 
                email=user['email'], 
                profile_pic=user['profile_pic']
            )
            return user
        except sqlite3.Error as e:
            print(f"Error fetching user by email: {e}")
            return None
        finally:
            if db:
                db.close()

    def __repr__(self):
        return f'<User {self.email}>'