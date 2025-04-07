from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import sys
import tempfile
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATA_FILE = 'users.txt'
TASKS = [
    {'id': 1, 'title': 'Hello World', 'category': 'Основы', 'description': 'Выведите "Hello, World!"',
     'tests': [{'input': None, 'output': 'Hello, World!'}]},
    {'id': 2, 'title': 'Сумма чисел', 'category': 'Алгоритмы', 'description': 'Функция sum(a, b)',
     'tests': [{'input': 'sum(2,3)', 'output': '5'}, {'input': 'sum(-1,1)', 'output': '0'}]},
    {'id': 3, 'title': 'Факториал', 'category': 'Алгоритмы', 'description': 'Функция factorial(n)',
     'tests': [{'input': 'factorial(5)', 'output': '120'}, {'input': 'factorial(0)', 'output': '1'}]},
    {'id': 4, 'title': 'Палиндром', 'category': 'Строки', 'description': 'Проверка палиндрома',
     'tests': [{'input': 'is_palindrome("madam")', 'output': 'True'},
               {'input': 'is_palindrome("python")', 'output': 'False'}]},
    {'id': 5, 'title': 'Фибоначчи', 'category': 'Алгоритмы', 'description': 'Функция fibonacci(n)',
     'tests': [{'input': 'fibonacci(10)', 'output': '55'}, {'input': 'fibonacci(1)', 'output': '1'}]},
    {'id': 6, 'title': 'Калькулятор', 'category': 'Основы', 'description': 'Функция calculate(a, b, op)',
     'tests': [{'input': 'calculate(4,2,"+")', 'output': '6'}, {'input': 'calculate(4,2,"/")', 'output': '2.0'}]},
    {'id': 7, 'title': 'Максимум списка', 'category': 'Списки', 'description': 'Функция find_max()',
     'tests': [{'input': 'find_max([1,5,3])', 'output': '5'}, {'input': 'find_max([])', 'output': 'None'}]},
    {'id': 8, 'title': 'Сортировка пузырьком', 'category': 'Алгоритмы', 'description': 'Функция bubble_sort()',
     'tests': [{'input': 'bubble_sort([3,1,4,1,5,9])', 'output': '[1,1,3,4,5,9]'},
               {'input': 'bubble_sort([])', 'output': '[]'}]},
    {'id': 9, 'title': 'Простое число', 'category': 'Математика', 'description': 'Функция is_prime(n)',
     'tests': [{'input': 'is_prime(7)', 'output': 'True'}, {'input': 'is_prime(4)', 'output': 'False'}]},
    {'id': 10, 'title': 'FizzBuzz', 'category': 'Циклы', 'description': 'Функция fizzbuzz(n)',
     'tests': [{'input': 'fizzbuzz(5)', 'output': '1\n2\nFizz\n4\nBuzz'}]},
    {'id': 11, 'title': 'Обращение строки', 'category': 'Строки', 'description': 'Функция reverse_string()',
     'tests': [{'input': 'reverse_string("hello")', 'output': 'olleh'},
               {'input': 'reverse_string("12345")', 'output': '54321'}]},
    {'id': 12, 'title': 'Подсчет слов', 'category': 'Строки', 'description': 'Функция count_words()',
     'tests': [{'input': 'count_words("Hello world")', 'output': '2'}, {'input': 'count_words("")', 'output': '0'}]},
    {'id': 13, 'title': 'Удаление дубликатов', 'category': 'Списки', 'description': 'Функция remove_duplicates()',
     'tests': [{'input': 'remove_duplicates([1,2,2,3])', 'output': '[1,2,3]'},
               {'input': 'remove_duplicates(["a","a","b"])', 'output': "['a','b']"}]},
    {'id': 14, 'title': 'Анаграмма', 'category': 'Строки', 'description': 'Функция is_anagram()',
     'tests': [{'input': 'is_anagram("listen","silent")', 'output': 'True'},
               {'input': 'is_anagram("hello","world")', 'output': 'False'}]},
    {'id': 15, 'title': 'НОД', 'category': 'Математика', 'description': 'Функция gcd(a, b)',
     'tests': [{'input': 'gcd(54,24)', 'output': '6'}, {'input': 'gcd(17,5)', 'output': '1'}]},
    {'id': 16, 'title': 'Двоичное число', 'category': 'Конвертация', 'description': 'Функция to_binary(n)',
     'tests': [{'input': 'to_binary(5)', 'output': '101'}, {'input': 'to_binary(0)', 'output': '0'}]},
    {'id': 17, 'title': 'Четность', 'category': 'Условия', 'description': 'Функция is_even(n)',
     'tests': [{'input': 'is_even(4)', 'output': 'True'}, {'input': 'is_even(7)', 'output': 'False'}]},
    {'id': 18, 'title': 'Сумма цифр', 'category': 'Математика', 'description': 'Функция sum_digits(n)',
     'tests': [{'input': 'sum_digits(123)', 'output': '6'}, {'input': 'sum_digits(0)', 'output': '0'}]},
    {'id': 19, 'title': 'Минимум списка', 'category': 'Списки', 'description': 'Функция find_min()',
     'tests': [{'input': 'find_min([5,3,8,1])', 'output': '1'}, {'input': 'find_min([])', 'output': 'None'}]},
    {'id': 20, 'title': 'Среднее арифметическое', 'category': 'Математика', 'description': 'Функция average()',
     'tests': [{'input': 'average([1,2,3])', 'output': '2.0'}, {'input': 'average([])', 'output': '0'}]},
    {'id': 21, 'title': 'Гласные буквы', 'category': 'Строки', 'description': 'Функция count_vowels()',
     'tests': [{'input': 'count_vowels("Hello World")', 'output': '3'},
               {'input': 'count_vowels("Python")', 'output': '2'}]},
    {'id': 22, 'title': 'Генератор паролей', 'category': 'Генерация', 'description': 'Функция generate_password()',
     'tests': [{'input': 'len(generate_password())', 'output': '8'}]},
    {'id': 23, 'title': 'Валидация email', 'category': 'Проверка', 'description': 'Функция validate_email()',
     'tests': [{'input': 'validate_email("test@example.com")', 'output': 'True'},
               {'input': 'validate_email("invalid")', 'output': 'False'}]},
    {'id': 24, 'title': 'Поиск подстроки', 'category': 'Строки', 'description': 'Функция find_substrings()',
     'tests': [{'input': 'find_substrings("ababa","aba")', 'output': '[0, 2]'},
               {'input': 'find_substrings("test","no")', 'output': '[]'}]},
    {'id': 25, 'title': 'Шифр Цезаря', 'category': 'Шифрование', 'description': 'Функция caesar_cipher()',
     'tests': [{'input': 'caesar_cipher("abc",1)', 'output': 'bcd'},
               {'input': 'caesar_cipher("xyz",3)', 'output': 'abc'}]},
    {'id': 26, 'title': 'Квадратное уравнение', 'category': 'Математика',
     'description': 'Функция solve_quadratic(a,b,c)',
     'tests': [{'input': 'solve_quadratic(1,-3,2)', 'output': '[2.0, 1.0]'},
               {'input': 'solve_quadratic(1,2,1)', 'output': '[-1.0]'}]},
    {'id': 27, 'title': 'Цельсии в Фаренгейты', 'category': 'Конвертация',
     'description': 'Функция celsius_to_fahrenheit()',
     'tests': [{'input': 'celsius_to_fahrenheit(0)', 'output': '32.0'},
               {'input': 'celsius_to_fahrenheit(100)', 'output': '212.0'}]},
    {'id': 28, 'title': 'Генератор штрих-кодов', 'category': 'Генерация', 'description': 'Функция generate_barcode()',
     'tests': [{'input': 'generate_barcode(123456789012)', 'output': 'Valid EAN13'}]},
    {'id': 29, 'title': 'Максимум матрицы', 'category': 'Матрицы', 'description': 'Функция matrix_max()',
     'tests': [{'input': 'matrix_max([[1,2],[3,4]])', 'output': '4'},
               {'input': 'matrix_max([[-5,-2],[-3,-10]])', 'output': '-2'}]},
    {'id': 30, 'title': 'Транспонирование', 'category': 'Матрицы', 'description': 'Функция transpose()',
     'tests': [{'input': 'transpose([[1,2],[3,4]])', 'output': '[[1,3],[2,4]]'},
               {'input': 'transpose(<button class="citation-flag" data-index="5">)',
                'output': '<button class="citation-flag" data-index="5">'}]}
]


def load_users():
    users = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    login, pwd_hash, reg_date, stats = parts
                    users[login] = {
                        'password': pwd_hash,
                        'reg_date': reg_date,
                        'stats': eval(stats) if stats else {}
                    }
    return users


def save_users(users):
    with open(DATA_FILE, 'w') as f:
        for login, data in users.items():
            f.write(f"{login}|{data['password']}|{data['reg_date']}|{repr(data.get('stats', {}))}\n")


def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/')
@login_required
def index():
    categories = {}
    for task in TASKS:
        categories.setdefault(task['category'], []).append(task)
    return render_template('index.html', categories=categories, user=session['user'])


@app.route('/task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    selected_task = next((t for t in TASKS if t['id'] == task_id), None)

    if request.method == 'POST':
        code = request.form['code']
        results = []
        success_count = 0

        for test in selected_task['tests']:
            with tempfile.NamedTemporaryFile(suffix='.py', mode='w+', delete=False) as tmp:
                tmp.write(code)
                if test['input']:
                    tmp.write(f"\nprint({test['input']})")
                tmp.flush()

                try:
                    result = subprocess.run(
                        [sys.executable, tmp.name],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )

                    output = result.stdout.strip()
                    error = result.stderr.strip()

                    if not error and output == test['output']:
                        success_count += 1
                        results.append({
                            'success': True,
                            'message': f"✅ Тест пройден: {test['input'] or 'основной код'}"
                        })
                    else:
                        msg = error or f"❌ Неверный вывод: {output}"
                        results.append({'success': False, 'message': msg})

                except subprocess.TimeoutExpired:
                    results.append({'success': False, 'message': '❌ Превышено время выполнения'})

        if success_count == len(selected_task['tests']):
            current_user = session['user']
            current_user['stats'][task_id] = current_user['stats'].get(task_id, 0) + 1

            users = load_users()
            users[current_user['login']]['stats'] = current_user['stats']
            save_users(users)

        return jsonify(results)

    return render_template('task.html', task=selected_task)


@app.route('/profile')
@login_required
def profile():
    user = session['user']
    return render_template('profile.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        users = load_users()
        user_data = users.get(login)

        if user_data and check_password_hash(user_data['password'], password):
            session['user'] = {
                'login': login,
                'reg_date': user_data['reg_date'],
                'stats': user_data.get('stats', {})
            }
            return redirect(url_for('index'))

        return render_template('auth/login.html', error='Неверные данные')

    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        confirm = request.form['confirm']
        users = load_users()

        if login in users:
            return render_template('auth/register.html', error='Логин занят')
        if password != confirm:
            return render_template('auth/register.html', error='Пароли не совпадают')

        password_hash = generate_password_hash(password)
        reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        users[login] = {
            'password': password_hash,
            'reg_date': reg_date,
            'stats': {}
        }
        save_users(users)

        return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
      app.run(host='127.0.0.1', port=8080)