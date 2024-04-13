from flask import Flask, render_template, request, redirect, url_for
from models import UserInteraction


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/createprofile')
def createprofile():
    return render_template('createprofile.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/profile')
def profile():
    user_interaction = UserInteraction()
    user, recipes = user_interaction.login("test", "test")
    return render_template('profile.html', title='Profile', user=user, recipes=recipes)


@app.route('/search')
def search():
    return render_template('search.html')




if __name__ == '__main__':
    app.run(debug=True)