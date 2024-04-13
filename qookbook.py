from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import UserInteraction


app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/createprofile')
def createprofile():
    return render_template('createprofile.html')


@login_manager.user_loader
def load_user(user_id):
    user_interaction = UserInteraction()
    return user_interaction.user_manipulation.get_user_object(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_interaction = UserInteraction()
        user = user_interaction.login(username, password)
        if user:
            login_user(user, remember=True)
            return redirect(url_for('profile'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    user = current_user
    user_interaction = UserInteraction()
    recipes = user_interaction.get_fav_recipes(user.id)
    return render_template('profile.html', title='Profile', user=user, recipes=recipes)


@app.route('/search')
def search():
    return render_template('search.html')




if __name__ == '__main__':
    app.run(debug=True)