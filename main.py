from flask import Flask, request, redirect,render_template,jsonify,session

app = Flask(__name__)
users = []
def check_auth(username, password):
    return username == 'admin' and password == 'password123'

def authenticate():
    return redirect('/login')

@app.route('/')
def index():
    return 'вы не авторизованы'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_auth(username, password):
            return redirect('/about')
        else:
            return 'неверные данные.'
    return render_template('login.html')

@app.route('/about')
def about():
    return redirect('/users')


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    if username:
        users.append(username)
        return jsonify({'message': 'User added successfully'})
    else:
        return jsonify({'error': 'Username is required'})

@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        users.remove(username)
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'})

if __name__ == '__main__':
    app.run()
