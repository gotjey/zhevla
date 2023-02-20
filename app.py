from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/nikita')
def index():
    return 'Hello Nikita!'

if __name__ == '__main__':
    app.run()