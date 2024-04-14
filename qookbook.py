from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import UserInteraction


app = Flask(__name__)
app.secret_key = 'secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    user_interaction = UserInteraction()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return "Passwords do not match"
        else:
            user = user_interaction.create_user(username, password)
            login_user(user, remember=True)
            return redirect(url_for('profile'))
    return render_template('signup.html', title='Sign Up')


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
    return render_template('login.html', title='Login')


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


@app.route('/search', methods=['GET', 'POST'])
def search():
    user_interaction = UserInteraction()
    last_search = user_interaction.temp_recipe_manipulation.read_file()
    if request.method == 'POST':
        ingridients = request.form['search']
        recipes = user_interaction.search_recipes(ingridients)
        session['recipes'] = recipes
        return render_template('search.html', title='Search', recipes=recipes, last_search=last_search)
    return render_template('search.html', title='Search', last_search=last_search)


@app.route('/add_to_favorites', methods=['POST'])
@login_required
def add_to_favorites():
    user_interaction = UserInteraction()
    recipe_title = request.form['recipe_title']
    recipe = user_interaction.temp_recipe_manipulation.get_recipe_object(recipe_title)
    user_interaction.recipe_manipulation.add_fav_recipe(current_user.id, recipe)
    recipes = session.get('recipes')
    return render_template('search.html', title='Search', recipes=recipes)



if __name__ == '__main__':
    app.run(debug=True)