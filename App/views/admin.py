from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import jwt_required, current_user
from flask_admin import Admin
from flask import flash, redirect, url_for, request  # Added missing imports
from App.models import db, User

class AdminView(ModelView):

    @jwt_required()
    def is_accessible(self):
        return current_user is not None

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash("Login to access admin")
        return redirect(url_for('index_views.index_page', next=request.url))

def setup_admin(app):
    admin = Admin(app, name='FlaskMVC', template_mode='bootstrap3')
    admin.add_view(AdminView(User, db.session))