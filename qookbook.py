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
    """The index route is the home page of the application. It renders the index.html template."""
    return render_template('index.html', title='Home')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """The signup route is used to create a new user account. It renders the signup.html template."""
    user_interaction = UserInteraction()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash("Passwords do not match")
            return redirect(url_for('signup'))
        else:
            try:
                user = user_interaction.create_user(username, password)
                login_user(user, remember=True)
                return redirect(url_for('profile'))
            except Exception as e:
                flash(f"{e}")
                return redirect(url_for('signup'))
    return render_template('signup.html', title='Sign Up')


@login_manager.user_loader
def load_user(user_id):
    """This function is used to load a user object from the user_id provided by the login manager."""
    user_interaction = UserInteraction()
    return user_interaction.user_manipulation.get_user_object(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """The login route is used to authenticate a user. It renders the login.html template."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_interaction = UserInteraction()
        try:
            user = user_interaction.login(username, password)
            login_user(user, remember=True)
            return redirect(url_for('profile'))
        except Exception as e:
            flash(f"{e}")
            return redirect(url_for('login'))
    return render_template('login.html', title='Login')


@app.route('/logout')
@login_required
def logout():
    """The logout route is used to log out a user. It redirects to the index route after logging out."""
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    """The profile route is used to display the user's profile page. It renders the profile.html template."""
    user = current_user
    user_interaction = UserInteraction()
    recipes = user_interaction.get_fav_recipes(user.id)
    return render_template('profile.html', title='Profile', user=user, recipes=recipes)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """The search route is used to search for recipes based on ingredients. It renders the search.html template."""
    if request.method == 'POST':
        try:
            user_interaction = UserInteraction()
            ingredients = request.form['search']
            recipes = user_interaction.search_recipes(ingredients)
            session['recipes'] = [recipe for recipe in recipes]
            return render_template('search.html', title='Search', recipes=recipes)
        except Exception as e:
            flash(f"{e}")
            return render_template('search.html', title='Search')
    return render_template('search.html', title='Search')


@app.route('/add_to_favorites', methods=['POST'])
@login_required
def add_to_favorites():
    """The add_to_favorites route is used to add a recipe to the user's favorites. It redirects to the search route after adding the recipe."""
    recipe_title = request.form['recipe_title']
    recipes = session.get('recipes')
    recipe = next((recipe for recipe in recipes if recipe['title'] == recipe_title), None)
    if recipe:
        user_interaction = UserInteraction()
        user_interaction.add_fav_recipe(current_user.id, **recipe)
        flash('Recipe successfully added to favorites!')
    else:
        flash('Something went wrong. Try again')
    return render_template('search.html', title='Search', recipes=recipes)



if __name__ == '__main__':
    app.run(debug=True)