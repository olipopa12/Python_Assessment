
from flask import Flask, flash, redirect, request, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = "mysecretkey" #A secret key is required to use CSRF.

login_manager = LoginManager()
login_manager.init_app(app)


#used to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#login page
@app.route('/', methods=['GET', 'POST'])
def index():
    
    #Task.__table__.drop(db.engine)
    db.create_all() #creates all tables if not exist
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('tasks',page=1))
        else:
                return render_template('error.html', error=1)       
    return render_template('login.html', form=form)
   

#logout
@app.route("/logout", methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

#registration page
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

#tasks page
@app.route('/tasks/<int:page>', methods=['GET'])
def tasks(page):
    #page = request.args.get('page', 1, type=int)
    tasks = Task.query.where(Task.user_id == User.get_id(current_user))
    pagination=tasks.paginate(page=page, per_page=2) # 2 tasks per page
    return render_template('tasks.html', tasks=list(tasks), pagination=pagination)

#add new task
@app.route('/add',methods=['GET','POST'])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        t = Task(user_id=User.get_id(current_user), title=form.title.data, description=form.description.data, completition_status=False)
        db.session.add(t)
        db.session.commit()
        flash('Task added to the database')
        return redirect(url_for('tasks',page=1))
    return render_template('add.html',form=form)

#edit a task
@app.route('/edit/<int:task_id>',methods=['GET','POST'])
def edit(task_id):
    task = Task.query.get(task_id)
    form = TaskForm()
    if form.validate_on_submit():
            task.title = form.title.data
            task.description = form.description.data
            db.session.commit()
            return redirect(url_for('tasks',page=1))
    form.title.data = task.title
    form.description.data = task.description
    return render_template('edit.html',form=form, task_id=task_id)

#update a task to completed    
@app.route('/complete/<int:task_id>',methods=['GET','PUT'])
def complete(task_id):
    task = Task.query.get(task_id)
    task.completition_status=True
    db.session.commit()
    return redirect(url_for('tasks',page=1))

#delete a task
@app.route('/delete=/<int:task_id>',methods=['GET','DELETE'])
def delete(task_id):
     task = Task.query.get(task_id)
     db.session.delete(task)
     db.session.commit()
     return redirect(url_for('tasks',page=1))

#handle server error
@app.errorhandler(500)
def server_error(e):
  db.session.rollback() #resets the session to a clean state
  return render_template('error.html', error=2)

#handle not found error
@app.errorhandler(404)
def server_error(e):
  return render_template('error.html', error=3)


############################### MODELS ####################################################

#user model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    

#task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)    
    completition_status=db.Column(db.Boolean(), nullable=False)

#the login form
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

#the registration form
class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')   

#form for adding new tasks
class TaskForm(FlaskForm):
    title = StringField(validators=[
                           InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "Title"})

    description = StringField(validators=[
                             InputRequired(), Length(min=10, max=200)], render_kw={"placeholder": "Description"})

    add = SubmitField('Add')     

    edit = SubmitField('Edit') 



#run the application
if __name__ == '__main__':
   app.run(debug=True)