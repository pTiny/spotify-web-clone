from flask import Flask
from website import pages_routes, auth_routes, details


app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
app.config['SECRET_KEY'] = details.creds['SKey']


app.register_blueprint(auth_routes.auth_bp, url_prefix='/')
app.register_blueprint(pages_routes.pages_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(debug=True)