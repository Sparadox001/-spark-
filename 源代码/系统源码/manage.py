# _*_ codding:utf-8 _*_
from app import create_app

app = create_app('default')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    # app.run()