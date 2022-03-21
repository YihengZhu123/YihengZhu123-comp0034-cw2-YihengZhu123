from blogapp.models import Profile
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from blogapp.models import User

user_bp = Blueprint('user', __name__)
