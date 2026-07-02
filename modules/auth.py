import streamlit as st
import bcrypt
import json
from datetime import datetime, timedelta

class AuthManager:
    """Manage user authentication and sessions"""
    
    def __init__(self):
        self.users_file = "data/users.json"
        self.ensure_storage()
    
    def ensure_storage(self):
        """Ensure data storage directory and files exist"""
        import os
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode(), hashed.encode())
    
    def load_users(self) -> dict:
        """Load all users from storage"""
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except:
            return {}
    
    def save_users(self, users: dict):
        """Save users to storage"""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)
    
    def user_exists(self, email: str) -> bool:
        """Check if user already exists"""
        users = self.load_users()
        return email.lower() in users
    
    def signup(self, email: str, name: str, password: str, grade_level: str) -> tuple:
        """Register a new user"""
        email = email.lower().strip()
        
        if self.user_exists(email):
            return False, "Email already registered"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        users = self.load_users()
        users[email] = {
            "name": name,
            "password": self.hash_password(password),
            "grade_level": grade_level,
            "created_at": datetime.now().isoformat(),
            "preferences": {
                "language": "en",
                "theme": "light",
                "subjects": []
            }
        }
        
        self.save_users(users)
        return True, "Signup successful"
    
    def login(self, email: str, password: str) -> tuple:
        """Authenticate user credentials"""
        email = email.lower().strip()
        users = self.load_users()
        
        if email not in users:
            return False, "Invalid email or password", {}
        
        user = users[email]
        if not self.verify_password(password, user["password"]):
            return False, "Invalid email or password", {}
        
        # Create session
        session_data = {
            "email": email,
            "name": user["name"],
            "grade_level": user["grade_level"],
            "preferences": user["preferences"],
            "login_time": datetime.now().isoformat()
        }
        
        return True, "Login successful", session_data
    
    def update_user(self, email: str, updates: dict) -> tuple:
        """Update user information"""
        email = email.lower()
        users = self.load_users()
        
        if email not in users:
            return False, "User not found"
        
        for key, value in updates.items():
            if key == "password":
                users[email][key] = self.hash_password(value)
            else:
                users[email][key] = value
        
        self.save_users(users)
        return True, "User updated successfully"
    
    def get_user(self, email: str) -> dict:
        """Get user information"""
        users = self.load_users()
        email = email.lower()
        return users.get(email, {})
    
    def is_session_valid(self) -> bool:
        """Check if current session is valid"""
        if "user_session" not in st.session_state:
            return False
        
        session = st.session_state.user_session
        login_time = datetime.fromisoformat(session.get("login_time", datetime.now().isoformat()))
        
        # Session expires after 1 hour
        if datetime.now() - login_time > timedelta(hours=1):
            return False
        
        return True
    
    def logout(self):
        """Clear user session"""
        if "user_session" in st.session_state:
            del st.session_state.user_session
