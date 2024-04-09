from flask import Flask, render_template
from insert_data import get_data

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', content=users)


if __name__ == '__main__':
    users = get_data()
    app.run(debug=True)
