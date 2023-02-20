from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import yaml
from flask_mysqldb import MySQL
import requests
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
Bootstrap(app)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        form = request.form
        name = form['name']
        password = form['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employee(name, age) VALUES(%s,%s)", (password, name))
        mysql.connection.commit()
    return render_template('index.html')

@app.route('/employees')
def employee():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM employee")
    if result_value:
        employees = cursor.fetchall()
        return render_template('employees.html', employees=employees)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/weather')
def weather():
    # список міст, для яких потрібно отримати погоду
    cities = ['Uman\'', 'Winnipeg', 'Halifax']

    # ваш ключ API OpenWeatherMap
    api_key = 'ff659fcd92d95f0e223bec0e9ad745bc'

    # список, де зберігаємо інформацію про погоду для кожного міста
    weather_data = []

    # цикл по кожному місту, щоб отримати інформацію про погоду
    for city in cities:
        # формуємо URL для запиту до API OpenWeatherMap
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        # виконуємо запит до API і зберігаємо відповідь в змінну response
        response = requests.get(url)

        # отримуємо JSON-об'єкт з відповіддю API
        json_data = response.json()
        # дістаємо потрібні дані про погоду з JSON-об'єкту
        city_weather = {
            'city': city,
            'temperature': json_data['main']['temp'],
            'description': json_data['weather'][0]['description'],
            'icon': json_data['weather'][0]['icon'],
            'feel': json_data['main']['feels_like']
        }

        # додаємо інформацію про погоду для цього міста в список weather_data
        weather_data.append(city_weather)

    # відображаємо шаблон і передаємо список з інформацією про погоду для кожного міста
    return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
