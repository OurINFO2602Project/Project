from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
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
  specialization = db.Column(db.String(120), nullable=True)
  _mapper_args_ = {
      'polymorphic_identity': 'student',
  }

  def _init_(self, username, name, email, password, gpa, degree, graduation_year, specialization):
    super()._init_(username, name, email, password)
    self.gpa = gpa
    self.degree = degree
    self.graduation_year = graduation_year
    self.specialization = specialization
=======
  __tablename__ = 'student'
  __mapper_args__ = {
      'polymorphic_identity': 'student',
  }

  def __init__(self, username, name, email, password):
    super().__init__(username, name, email, password)
>>>>>>> e5f27b44394556a5c60c8002171e5cb73b49387a

  def apply_internship(self, internship, file="dummyfilestring"):
    new_application = Application(internship, self, file)
    self.applications.append(new_application)
    return new_application

class Company(User):
  __tablename__ = 'company'
  __mapper_args__ = {
      'polymorphic_identity': 'company',
  }

  def __init__(self, username, name, email, password):
    super().__init__(username, name, email, password)

  def create_internship(self, title, description, salary):
    newinternship = Internship(title, description, salary)
    self.internships.append(newinternship)
    return newinternship

  def update_app(self, app, status):
    if app.internship.company == self:
      app.status = status
      db.session.commit()
    
class Staff(User):
  __tablename__ = 'staff'
  __mapper_args__ = {
      'polymorphic_identity': 'staff',
  }

  def __init__(self, username, name, email, password):
    super().__init__(username, name, email, password)
    
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
    self.resume_url =  url

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
    student = db.relationship('Student', backref=db.backref('shortlists', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('shortlisted_students', lazy=True))
    
    def get_json(self):
        return {
            "id": self.id,
            "internship_id": self.internship_id,
            "internship": self.internship.title,
            "student_id": self.student_id,
            "student": self.student.username,
        }
