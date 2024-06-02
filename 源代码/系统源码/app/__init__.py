from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    # 注册蓝图
    from app.views.home import home
    from app.views.portal import portal
    from app.views.visualpic import visualpic
    app.register_blueprint(home)
    app.register_blueprint(portal)
    app.register_blueprint(visualpic)

    return app