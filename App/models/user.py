from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=True)  # Changed to nullable=True to be compatible with existing code
    email = db.Column(db.String(120), unique=True, nullable=True)  # Changed to nullable=True to be compatible with existing code
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, password, name=None, email=None):
        self.username = username
        self.name = name if name else username  # Default name to username if not provided
        self.email = email if email else f"{username}@example.com"  # Default email if not provided
        self.set_password(password)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.id} {self.username} - {self.email}>'

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "type": self.type
        }

class Student(User):
    gpa = db.Column(db.Float, nullable=True)
    degree = db.Column(db.String(120), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, name=None, email=None, gpa=None, degree=None, graduation_year=None):
        super().__init__(username, password, name, email)
        self.gpa = gpa
        self.degree = degree
        self.graduation_year = graduation_year

    def apply_internship(self, internship, file="dummyfilestring"):
        new_application = Application(internship, self, file)
        self.applications.append(new_application)
        return new_application

class Company(User):
    __mapper_args__ = {
        'polymorphic_identity': 'company',
    }

    def __init__(self, username, password, name=None, email=None):
        super().__init__(username, password, name, email)

    def create_internship(self, title, description, salary, start_date="TBD", end_date="TBD"):
        newinternship = Internship(title, description, start_date, end_date, salary)
        self.internships.append(newinternship)
        return newinternship

    def update_app(self, app, status):
        if app.internship.company == self:
            app.status = status
            db.session.commit()

class Staff(User):
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, username, password, name=None, email=None):
        super().__init__(username, password, name, email)

    def create_shortlist(self, student, internship):
        shortlist_entry = Shortlist(student=student, internship=internship)
        db.session.add(shortlist_entry)
        db.session.commit()
        return shortlist_entry

class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('internships', lazy=True))

    def __init__(self, title, description, start_date, end_date, salary):
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.salary = salary

    def get_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "start date": self.start_date,
            "end date": self.end_date,
            "description": self.description,
            "salary": self.salary,
        }

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(80), nullable=False, default='pending')
    resume_url = db.Column(db.String(120), nullable=False)
    student = db.relationship('Student', backref=db.backref('applications', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('applications', lazy=True))

    def __init__(self, internship, student, url="https://file.pdf"):
        self.internship = internship
        self.student = student
        self.resume_url = url

    def get_json(self):
        return {
            "id": self.id,
            "internship_id": self.internship_id,
            "internship": self.internship.title,
            "student_id": self.student_id,
            "student": self.student.username,
            "status": self.status,
            "resume_url": self.resume_url
        }

class Shortlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    student = db.relationship('Student', foreign_keys=[student_id], backref=db.backref('shortlists', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('shortlisted_students', lazy=True))
    staff = db.relationship('Staff', foreign_keys=[staff_id])

    def get_json(self):
        return {
            "id": self.id,
            "internship_id": self.internship_id,
            "internship": self.internship.title,
            "student_id": self.student_id,
            "student": self.student.username,
        }