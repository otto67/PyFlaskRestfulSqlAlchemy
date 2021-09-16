from flask import Flask, jsonify, render_template, Response, request, Blueprint, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3, secrets, string, random
from flask_restful import Resource, Api
from . import db
from .models import Task, User
from flask_login import login_required, current_user
from flask import flash
from functools import wraps

my_app = Blueprint('my_app', __name__)

api = Api(my_app)

""" Decorator for routes requiring that the user has admin status."""
def is_auth_and_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin:
            return func(*args, **kwargs)
        else:
            flash("Not allowed. You are not an administrator", "warning")
            return {'message': 'No access, you are not an administrator',
            'errno':1}
    return wrapper


# Main page
class Index(Resource):
    def get(self):
        return Response(response=render_template('index.html'))       

# API for promoting and deleting users
class EditUsers(Resource):
    method_decorators = {
        'get':[login_required], 
        'delete':[is_auth_and_admin, login_required],
        'put':[is_auth_and_admin, login_required]
        }
    
    def get(self):
        return Response(response=render_template('useradm.html')) 
                      
    def delete(self, *args, **kwargs):
        
        json_data = request.get_json(force=True)
        id = json_data['id']
        if (id == 'all'):
            return delete_all_users()
        else:
            return delete_user(id)
    
    def put(self):
        json_data = request.get_json(force=True)
        id = json_data['id']      
        return toggle_user_status(id)

# API for listing users
class ListUsers(Resource):
    def get(self, id):
        if (id == 'all'):
            return get_all_users()
        else: 
            return get_user(id) 


class AddUser(Resource):
    method_decorators = {
        'post':[is_auth_and_admin, login_required], 
        }
          
    def post(self, *args, **kwargs):
        
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        admin = True if request.form.get('administrator') else False

        return add_user(email, name, password, admin)
            
# API for manipulating tasks and listing non-completed tasks 
class EditTasks(Resource):
    
    method_decorators = {
        'get':[login_required], 
        'delete':[login_required],
        'put':[login_required]
        }

    def get(self):
        return get_noncomplete_tasks()

    def put(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        if (id == 'all'):
            return complete_all_tasks()
        else:
            return complete_task(id)
    
    def post(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        user_id = json_data['user_id']
        return add_task(id, user_id)
    
    def delete(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        if (id == 'all'):
            return delete_all_tasks()
        else:
            return delete_task(id)

# Class for listing tasks
class ListTasks(Resource):
    method_decorators = {
        'get':[login_required]
        }
    def get(self, id):
        if (id == 'all'):
            return get_all_tasks()
        else: 
            return get_task(id) 

# API for user profile
class UserProfile(Resource):
    method_decorators = {'get': [login_required]}
    def get(self, *args, **kwargs):
        return Response(response=render_template('profile.html', user_data=current_user.name)) 

api.add_resource(Index, '/', '/index')

api.add_resource(EditUsers, '/editusers') # Requested through JavaScript fetch

api.add_resource(AddUser, '/user') # Requested via HTML post  
api.add_resource(EditTasks, '/task')
api.add_resource(ListUsers, '/listuser/<id>')
api.add_resource(ListTasks, '/listtask/<id>')

api.add_resource(UserProfile, '/profile')

def create_tables():
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS task (
        id integer PRIMARY KEY,
        desc text NOT NULL,
        complete boolean,
        user_id integer NOT NULL
    )""")
    conn.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS user (
        id integer PRIMARY KEY,
        email text NOT NULL,
        name text NOT NULL,
        password text NOT NULL,
        admin boolean
    )""")
    conn.commit()

    conn.close()


def add_user(email, name, password, admin):
    create_tables()

    if not email:
        flash('Please check your input data and try again.')
        return redirect(url_for('my_app.userprofile')) 

    user = User.query.filter_by(email=email).first()
    if user:
        flash('User already exists')
        return redirect(url_for('my_app.userprofile')) 

    user = User(email=email, name=name, password=password, admin=admin)

    db.session.add(user)
    db.session.commit()
   
    flash('Added new user with name ' + name)
    return redirect(url_for('my_app.userprofile')) 


def delete_user(id):
 
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})

    if (int(id) == 1):
        msg = f'Cannot delete user id 1'
        return jsonify({'message' : msg})

    user = User.query.filter_by(id=id).first()
    if not user:
        msg =  f'User with id {id} doesn\'t exist'
        return jsonify({'message' : msg})

    db.session.delete(user)    
    db.session.commit()
   
    msg = f'Deleted user with id {id}'
    return jsonify({'message' : msg})

def delete_all_users():
 
    all_users = User.query.all()
    num_rows = len(all_users)

    for user in all_users:
        db.session.delete(user)

    db.session.commit()
    
    msg = f'Deleted {num_rows} users from database'
    return jsonify({'message' : msg})

def toggle_user_status(id):
    
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})  

    if (int(id) == 1):
        msg = f'Cannot delete admin status for user id 1'
        return jsonify({'message' : msg})

    user = User.query.filter_by(id=id).first()
    
    if not user:
        msg =  f'No user with id {id}'
        return jsonify({'message' : msg})

    setattr(user, 'admin', not user.admin)
    
    db.session.commit()

    msg =  f'Modified user with id {id}'
    return jsonify({'message' : msg})

def get_user(id):
    
    user = User.query.filter_by(id=id).first()
    msg = []

    if not user:
        tmp = int(id)
        tmp2 = str(-tmp)
        msg.append([tmp2, 0, "none", "none", False])
    else:
        msg.append([user.id, user.email, user.name, user.admin])

    return jsonify(msg)

def get_all_users():  

    all_users = User.query.all()  
    msg = []
    if not all_users:
        msg.append(["none"])
    else:
        for user in all_users:
            msg.append([user.id, user.email, user.name, user.admin])

    return jsonify(msg)

def add_task(id, user_id):
    create_tables()

    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})  

    task = Task.query.filter_by(id=id).first()
    if task:
        msg =  f'Task with id {id} already exists'
        return jsonify({'message' : msg})

# Note! Check if user with user_id exists

    # Just randomize the fields of the database for now
    desc = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(3))

    complete = bool(random.getrandbits(1))
    
    task = Task(id=id,desc=desc, complete=complete, user_id=int(user_id))

    db.session.add(task)
    db.session.commit()
   
    msg = f'Added task with id {id}'
    return jsonify({'message' : msg})

def delete_task(id):
 
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})

    task = Task.query.filter_by(id=id).first()
    if not task:
        msg =  f'Task with id {id} doesn\'t exist'
        return jsonify({'message' : msg})

    db.session.delete(task)    
    db.session.commit()
   
    msg = f'Deleted task with id {id}'
    return jsonify({'message' : msg})

def delete_all_tasks():
 
    all_tasks = Task.query.all()
    num_rows = len(all_tasks)

    for task in all_tasks:
        db.session.delete(task)

    db.session.commit()
    
    msg = f'Deleted {num_rows} tasks from database'
    return jsonify({'message' : msg})

def complete_task(id):
    
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})  

    task = Task.query.filter_by(id=id).first()
    
    if not task:
        msg =  f'No task with id {id}'
        return jsonify({'message' : msg})

    setattr(task, 'complete', True)
    
    db.session.commit()

    msg =  f'Modified task with id {id}'
    return jsonify({'message' : msg})

def complete_all_tasks():
    
    all_tasks = Task.query.all()  
    
    for task in all_tasks:       
        setattr(task, 'complete', True)
    
    db.session.commit()

    msg =  f'Completed all tasks'
    return jsonify({'message' : msg})

def get_task(id):
    
    task = Task.query.filter_by(id=id).first()
    msg = []

    if not task:
        tmp = int(id)
        tmp2 = str(-tmp)
        msg.append([tmp2, 0, "none", "none", False])
    else:
        msg.append([task.id, task.desc, task.complete, task.user_id])

    return jsonify(msg)

def get_all_tasks():  

    all_tasks = Task.query.all()  
    msg = []
    if not all_tasks:
        msg.append(["none"])
    else:
        for task in all_tasks:
            msg.append([task.id, task.desc, task.complete, task.user_id])

    return jsonify(msg)

def get_noncomplete_tasks(): 
    noncompleted_tasks = Task.query.filter_by(complete=False).all()
    
    if not noncompleted_tasks:
        return jsonify(["No data"])  
    
    msg = []
    for task in noncompleted_tasks:
        msg.append([task.id, task.desc, task.user_id])

    return jsonify(msg)