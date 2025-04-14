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

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(100))
    duration = db.Column(db.String(50))  # e.g., "3 months"
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    application_deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # company user
    is_active = db.Column(db.Boolean, default=True)
    
    applications = db.relationship('Application', backref='internship', lazy=True)
    
    def __init__(self, title, description, created_by, requirements=None, location=None, 
                 duration=None, start_date=None, end_date=None, application_deadline=None):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.location = location
        self.duration = duration
        self.start_date = start_date
        self.end_date = end_date
        self.application_deadline = application_deadline
        self.created_by = created_by
    
    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'location': self.location,
            'duration': self.duration,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by,
            'is_active': self.is_active
        }

