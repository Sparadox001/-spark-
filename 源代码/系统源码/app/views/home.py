from flask import Blueprint, render_template, url_for
# from flask_pymongo import PyMongo
# mongo = PyMongo(app, url="mongodb://localhost:27017/github")

home = Blueprint('home', __name__)


@home.errorhandler(404)
def page_not_found(error):
    return render_template('pages/404.html'), 404


@home.route("/")
@home.route("/index/")
def index():
    return render_template('index.html')


@home.route('/<path:page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except:
        return page_not_found(404)
