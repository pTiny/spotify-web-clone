import sys, os, hashlib as hs
from flask import Blueprint, redirect, url_for, render_template, request, flash, session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website.models import User
from website.pedidos import database_check

 
auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/", methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':

        username_email = request.form.get('email_username')
        password = request.form.get('password')

        session["user"] = username_email

        if database_check('users.db', 'userdata', username_email, username_email, hs.sha256(password.encode()).hexdigest()):
            # flash('Log In Successful', category='success')
            return redirect(url_for('pages.home_page'))
        else:
            # flash('Error Loggin In: Wrong Username or Password', category='error')
            return redirect(url_for('auth.sign_in'))
    
    return render_template("sign_in.html")

@auth_bp.route("/sign-up/", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        re_password = request.form.get('repassword')

        if (username != '') and (email != '') and (password != '') and (re_password != ''):
            if password == re_password:
                User(username, email, hs.sha256(password.encode()).hexdigest()).add_to_database()
                return redirect("/")
            else:
                # flash message & ask user to re-confirm password
                return render_template("sign_up.html")
        else:
            # flash message & ask user to re-confirm password
            return render_template("sign_up.html")

    return render_template("sign_up.html")

@auth_bp.route("/logout/")
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.sign_in'))