from flask import Flask, render_template
from insert_data import get_data
from collections import OrderedDict

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', content=users)


if __name__ == '__main__':
    users = get_data()
    users = [OrderedDict(zip(['customer_id', 'name', 'last_name',
                         'email', 'phone_number'], user)) for user in users]
    app.run(debug=True)
