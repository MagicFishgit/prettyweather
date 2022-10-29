import imp
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'q89o7h49bqf374y502uqvkajsfklasbfkbbebebebebebekjkadsfbrtq3r8359n8fyonhc9yt9348yufnp0w394nytfw9q84yhntf89o2734yhtp9f23y4pt9fu23hn4tp9237h4tp9v2'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app