from flask import Flask, request, redirect, render_template, jsonify, session, url_for
import requests
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
SECRET_KEY_FOR_DELETION = '12'
app = Flask(__name__)
app.secret_key = '12'
methods = {}
sessions = {}
session_id_counter = 1

# /delete_user/admin?secret_key=12
encryption_histories = {}
users = {
    '123': generate_password_hash('123'),
    'admin': generate_password_hash('123'),
}
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/delete_user/<username>')
def delete_user(username):
    secret_key = request.args.get('secret_key')
    if secret_key != SECRET_KEY_FOR_DELETION:
        return "Неверный секретный ключ", 403

    if username in users:
        del users[username]

        session['users'] = users
        return redirect(url_for('logout'))
    else:
        return "Пользователь не найден", 404

@app.route('/user_list')
def user_list():
    if 'username' in session:
        return render_template('user_list.html', users=users.keys())
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = generate_password_hash(password)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_hash = users.get(username)
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username
            return redirect(url_for('lobby'))
    return render_template('login.html')

@app.route('/lobby')
def lobby():
    if 'username' in session:
        user_name = session['username']
        return render_template('lobby.html',username=user_name)
    else:
        return redirect(url_for('login'))
def vigenere_cipher(text, key, encrypt=True):
    alphabet = ', . : (_) -0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    key_idx = 0
    result = ''

    for char in text:
        if char.upper() in alphabet:
            shift = alphabet.index(key[key_idx % len(key)].upper())
            if encrypt:
                result += alphabet[(alphabet.index(char.upper()) + shift) % 26]
            else:
                result += alphabet[(alphabet.index(char.upper()) - shift) % 26]
            key_idx += 1
        else:
            result = "неверные значения"

    return result


def caesar_cipher(text, shift, encrypt=True):
    alphabet = ', . : (_) -0123456789АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    result = ''

    for char in text:
        if char.upper() in alphabet:
            idx = alphabet.index(char.upper())
            if encrypt:
                idx = (idx + shift) % 26
            else:
                idx = (idx - shift) % 26
            result += alphabet[idx] if char.isupper() else alphabet[idx].lower()
        else:
            result = "неверные значения"

    return result


@app.route('/shifr', methods=['GET', 'POST'])
def shifr():
    result = ""
    method = ""
    if 'username' in session:
        username = session['username']
        if username not in encryption_histories:
            encryption_histories[username] = []

        if request.method == 'POST':
            text = request.form['text']
            key = request.form['key']
            method = request.form.get('method', 'vigenere')
            encrypt = request.form['action'] == 'encrypt'
            if method == 'caesar':
                shift = int(key) if key.isdigit() else 0
                result = caesar_cipher(text, shift, encrypt)
            elif method == 'vigenere':
                result = vigenere_cipher(text, key, encrypt)
            encryption_histories[username].append({
                'username': username,
                'text': text,
                'result': result,
                'method': method,
                'action': 'encrypt' if encrypt else 'decrypt',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

        return render_template('shifr.html', result=result, method=method,
                               encryption_history=encryption_histories[username])
    else:
        return redirect(url_for('login'))

@app.route('/encryption_history/<username>')
def encryption_history(username):
    if 'username' in session and username == session['username']:
        user_history = encryption_histories.get(username, [])
        for record in user_history:
            record['display_method'] = 'Цезарь' if record['method'] == 'caesar' else 'Виженер'
        return render_template('encryption_history.html', history=user_history)
    else:
        return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()
