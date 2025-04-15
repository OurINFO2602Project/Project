from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    profile = db.relationship('UserProfile', backref='user', lazy=True)

    def __init__(self, username, password, role):
        self.username = username
        self.set_password(password)
        self.role = role

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    university = db.Column(db.String(100))
    major = db.Column(db.String(100))
    gpa = db.Column(db.Float)
    company = db.Column(db.String(100))
    industry = db.Column(db.String(100))

    def __init__(self, first_name, last_name, email, phone=None, university, major, gpa, company, industry):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address
        self.university = university
        self.major = major
        self.gpa = gpa
        self.company = company
        self.industry = industry 

    def get_json(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'university': self.university,
            'major': self.major,
            'gpa': self.gpa,
            'company': self.company,
            'industry': self.industry
        }                                                                                   

class Company(UserProfile):
    __tablename__ = 'company'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100))

    def __init__(self, company_name, industry, website=None):
        super().__init__(first_name=None, last_name=None, email=None, phone=None, university=None, major=None, gpa=None, company=company_name, industry=industry)
        self.company_name = company_name
        self.industry = industry
        self.website = website

class Internship(Company):
    __tablename__ = 'internship'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)

    def __init__(self, position, start_date, end_date, description=None):
        super().__init__(company_name=None, industry=None)
        self.position = position
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
    

