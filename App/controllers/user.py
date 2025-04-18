from App.models import User
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def get_shortlisted_students(internship_id):
    from App.models import Shortlist, Student
    shortlists = Shortlist.query.filter_by(internship_id=internship_id).all()
    return [shortlist.student for shortlist in shortlists]

def get_student_details(student_id):
    from App.models import Student
    student = Student.query.get(student_id)
    if not student:
        return None
    return {
        'id': student.id,
        'name': student.name,
        'email': student.email,
        'degree': student.degree,
        'gpa': student.gpa,
        'graduation_year': student.graduation_year,
        'resume_url': next((app.resume_url for app in student.applications), None)
    }