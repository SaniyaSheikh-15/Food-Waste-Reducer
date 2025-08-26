from flask_login import UserMixin
from storage import users, donations
import uuid
from datetime import datetime

class User(UserMixin):
    def __init__(self, username, email, password_hash, role, name, phone=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role  # 'restaurant', 'citizen', 'ngo', 'driver'
        self.name = name
        self.phone = phone
        self.created_at = datetime.now()
    
    @staticmethod
    def get(user_id):
        """Get user by ID"""
        return users.get(user_id)
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        for user in users.values():
            if user.username == username:
                return user
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        for user in users.values():
            if user.email == email:
                return user
        return None
    
    def save(self):
        """Save user to storage"""
        users[self.id] = self
        return self

class Donation:
    def __init__(self, donor_id, donor_name, food_type, quantity, description, location, contact_phone):
        self.id = str(uuid.uuid4())
        self.donor_id = donor_id
        self.donor_name = donor_name
        self.food_type = food_type
        self.quantity = quantity
        self.description = description
        self.location = location
        self.contact_phone = contact_phone
        self.status = 'Pending'  # 'Pending', 'Claimed', 'Delivered'
        self.claimed_by = None
        self.claimed_by_name = None
        self.driver_id = None
        self.driver_name = None
        self.created_at = datetime.now()
        self.claimed_at = None
        self.delivered_at = None
    
    @staticmethod
    def get(donation_id):
        """Get donation by ID"""
        return donations.get(donation_id)
    
    @staticmethod
    def get_all():
        """Get all donations"""
        return list(donations.values())
    
    @staticmethod
    def get_by_status(status):
        """Get donations by status"""
        return [d for d in donations.values() if d.status == status]
    
    @staticmethod
    def get_by_donor(donor_id):
        """Get donations by donor"""
        return [d for d in donations.values() if d.donor_id == donor_id]
    
    @staticmethod
    def get_by_ngo(ngo_id):
        """Get donations claimed by NGO"""
        return [d for d in donations.values() if d.claimed_by == ngo_id]
    
    @staticmethod
    def get_by_driver(driver_id):
        """Get donations assigned to driver"""
        return [d for d in donations.values() if d.driver_id == driver_id]
    
    def claim(self, ngo_id, ngo_name):
        """Claim donation by NGO"""
        if self.status == 'Pending':
            self.status = 'Claimed'
            self.claimed_by = ngo_id
            self.claimed_by_name = ngo_name
            self.claimed_at = datetime.now()
            return True
        return False
    
    def assign_driver(self, driver_id, driver_name):
        """Assign driver to donation"""
        if self.status == 'Claimed':
            self.driver_id = driver_id
            self.driver_name = driver_name
            return True
        return False
    
    def mark_delivered(self):
        """Mark donation as delivered"""
        if self.status == 'Claimed' and self.driver_id:
            self.status = 'Delivered'
            self.delivered_at = datetime.now()
            return True
        return False
    
    def save(self):
        """Save donation to storage"""
        donations[self.id] = self
        return self
