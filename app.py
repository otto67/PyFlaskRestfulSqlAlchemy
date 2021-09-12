from flask import Flask, jsonify, render_template, Response, request
from flask_sqlalchemy import SQLAlchemy
import os, sqlite3, secrets, string, random
from flask_restful import Resource, Api

app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

api = Api(app)

# Use as decorator when authorization is added
def login_required(func):
    def inner(*args, **kwargs):
        print("Login is required")
        return func(*args, **kwargs)
    return inner

class Index(Resource):
    def get(self):
        return Response(response=render_template('index.html'))       

class EditUsers(Resource):
    
    def put(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        return modify_user(id)
          
    def post(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        return add_user(id)
    
    def delete(self):
        json_data = request.get_json(force=True)
        id = json_data['id']
        if (id == 'all'):
            return delete_all_users()
        else:
            return delete_user(id)

class ListUsers(Resource):
    def get(self, id):
        if (id == 'all'):
            return get_all_users()
        else: 
            return get_user(id) 

class EditTasks(Resource):
    
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

class ListTasks(Resource):
    def get(self, id):
        if (id == 'all'):
            return get_all_tasks()
        else: 
            return get_task(id) 

api.add_resource(Index, '/')
api.add_resource(EditUsers, '/user')
api.add_resource(EditTasks, '/task')
api.add_resource(ListUsers, '/listuser/<id>')
api.add_resource(ListTasks, '/listtask/<id>')

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(50))
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer)

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
        public_id text NOT NULL,
        name text NOT NULL,
        password text NOT NULL,
        admin boolean
    )""")
    conn.commit()

    conn.close()


def add_user(id):
    create_tables()

    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
        return jsonify({'message' : msg})  

    user = User.query.filter_by(id=id).first()
    if user:
        msg =  f'User with id {id} already exists'
        return jsonify({'message' : msg})

    # Just randomize the fields of the database for now
    public_id = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(3))

    name = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(12))

    password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                  for i in range(8))

    adm = bool(random.getrandbits(1))

    user = User(id=id, public_id=public_id, name=name, password=password, admin=adm)

    db.session.add(user)
    db.session.commit()
   
    msg = f'Added user with id {id}'
    return jsonify({'message' : msg})


def delete_user(id):
 
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
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

def modify_user(id):
    
    if (int(id) <= 0):
        msg =  f'Invalid id {id}'
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
        msg.append([user.id, user.public_id, user.name, user.password, user.admin])

    return jsonify(msg)

def get_all_users():  

    all_users = User.query.all()  
    msg = []
    if not all_users:
        msg.append(["none"])
    else:
        for user in all_users:
            msg.append([user.id, user.public_id, user.name, user.password, user.admin])

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

if __name__ == '__main__':
    app.run(debug=True)