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
    if request.method == 'POST':
        ingredients = request.form['search']
        recipes = user_interaction.search_recipes(ingredients)
        session['recipes'] = [recipe for recipe in recipes]
        return render_template('search.html', title='Search', recipes=recipes)
    return render_template('search.html', title='Search')


@app.route('/add_to_favorites', methods=['POST'])
@login_required
def add_to_favorites():
    recipe_title = request.form['recipe_title']
    recipes = session.get('recipes')
    recipe = next((recipe for recipe in recipes if recipe['title'] == recipe_title), None)
    if recipe:
        user_interaction = UserInteraction()
        user_interaction.add_fav_recipe(current_user.id, **recipe)
        flash('Recipe successfully added to favorites!')
    else:
        flash('Something went wrong')
    return render_template('search.html', title='Search', recipes=recipes)



if __name__ == '__main__':
    app.run(debug=True)