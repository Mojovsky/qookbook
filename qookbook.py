from flask import Flask, render_template, request, redirect, url_for
from models import UserInteraction


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    user_interaction = UserInteraction()
    user, recipes = user_interaction.login("test", "test")
    return render_template('index.html', title='Home', user=user, recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)