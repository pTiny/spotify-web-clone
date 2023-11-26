import sys, os, json as js
from flask import Blueprint, redirect, url_for, render_template, request, session
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from website.models import searchItem
from website.pedidos import fetch_user, search, like


pages_bp = Blueprint('pages', __name__)


@pages_bp.route("/home/", methods=['GET', 'POST'])
def home_page():
    if "user" in session:
        user = session["user"]
        
        if 'search' in request.form:
            item = request.form.get('search')
            return render_template("search_page.html", search=f'Showing results for: {item}', user=user, userdata=fetch_user(user, "users.db", 'userdata'), content=search(item))

        elif 'follow-button' in request.form:
            value = request.form.get('follow-button')
            like(js.loads(value), js.loads(value)['type'], user, "users.db", 'userdata')
            return redirect(url_for('pages.home_page'))

        return render_template("home_page.html", user=user, userdata=fetch_user(user, "users.db", 'userdata'))

    else:
        return redirect(url_for('auth.sign_in'))