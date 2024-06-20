from flask import Flask, request, redirect,render_template,jsonify,session, url_for
import requests
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'замените_на_секретный_ключ'

# Обновленный список пользователей и их паролей (в виде хэшей)
users = {
    '123': generate_password_hash('123'),
    'admin': generate_password_hash('123'),
    'user3': generate_password_hash('password3'),
    'user4': generate_password_hash('password4'),
    'user5': generate_password_hash('password5')
}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/delete_user/<username>')
def delete_user(username):
    # Создаем локальную копию словаря пользователей

    # Удаляем пользователя из локального словаря, если он существует
    if username in users:
        del users[username]
        # Обновляем сессию с новым словарем пользователей
        session['users'] = users
    # Перенаправляем на страницу с обновленным списком пользователей
    return redirect(url_for('user_list'))

@app.route('/user_list')
def user_list():

    # Проверяем, вошел ли пользователь в систему
    if 'username' in session:
        return render_template('user_list.html', users=users.keys())
    else:
        # Если пользователь не вошел, перенаправляем на страницу входа
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Удаляем пользователя из сессии
    session.pop('username', None)
    # Перенаправляем на главную страницу или страницу входа
    return redirect(url_for('login'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Добавляем пользователя, если его еще нет в списке
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
        # Проверяем, совпадает ли хэш пароля
        if user_hash and check_password_hash(user_hash, password):
            session['username'] = username
            return redirect(url_for('lobby'))
    return render_template('login.html')

@app.route('/lobby')
def lobby():
    user_name = session['username']
    # Проверяем, вошел ли пользователь в систему
    if 'username' in session:
        # Выводим HTML шаблон dashboard.html
        return render_template('lobby.html',username=user_name)
    else:
        # Если пользователь не вошел, перенаправляем на страницу входа
        return redirect(url_for('login'))


def vigenere_cipher(text, key, encrypt=True):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key_idx = 0
    result = ''

def vigenere_cipher(text, key, encrypt=True):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
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
            result += char

    return result


@app.route('/shifr', methods=['GET', 'POST'])
def shifr():
    result = ''
    if 'username' in session:
        if (request.method == 'POST') and ('username' in session):
            text = request.form['text']
            key = request.form['key']
            encrypt = request.form['action'] == 'encrypt'
            result = vigenere_cipher(text, key, encrypt)
        return render_template('shifr.html', result=result,users=users.keys())
    else:
        # Если пользователь не вошел, перенаправляем на страницу входа
        return redirect(url_for('login'))
    # Проверяем, вошел ли пользователь в систему





if __name__ == '__main__':
    app.run()
