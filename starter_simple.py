from flask import Flask

app = Flask(__name__)


@app.route('/get-many')
def get_many():
    """
    http://127.0.0.1:8080/get-many
    """
    return 'get_many'


@app.route('/get-one')
def get_one():
    """
    http://127.0.0.1:8080/get-one
    """
    return 'get_one'


@app.route('/create')
def create():
    """
    http://127.0.0.1:8080/create
    """
    return 'create'


@app.route('/delete')
def delete():
    """
    http://127.0.0.1:8080/delete
    """
    return 'delete'


@app.route('/update')
def update():
    """
    http://127.0.0.1:8080/update
    """
    return 'update'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

