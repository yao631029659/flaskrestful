from flask import Flask,render_template,request
from flask_restful import reqparse, abort, Api, Resource,fields,marshal_with
from config import DevConfig
from models import db,User

app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app)
db.init_app(app)
# 修改Jinja2的配置，让他只渲染空格之间的数据，而Vue.js处理不加空格的模板。
app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'
# 相当于数据库
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

# 如果不存在数据库就报错
# {
#   "message": "Todo todo2 doesn't exist. You have requested this URI [/todos/todo2] but did you mean /todos/<todo_id> or /todos ?"
# }
def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')
@app.route('/')
def index():
    return render_template('index.html')

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        # 找到最大的序列号 然后加1
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
post_fileds={
    'id':fields.Integer,
    'username':fields.String
}
class Userlist(Resource):
    @marshal_with(post_fileds)
    def get(self):
        user=User.query.all()
        return user

    def post(self):
        if not request.json:
            print('没有回传数据')
            abort(400)
        print('回传的数据是')
        print(request.json['id'])
        print(request.json['username'])
        #  request.json回传的数据是字典
        user=User(username=request.json['username'])
        print(request.json)
        db.session.add(user)
        db.session.commit()

class Users(Resource):
    def delete(self,user_id):
        print('删除被调用')
        print('user_id',user_id)
        # print(request.json) request 用json是收不到值的
        user=User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()


## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Userlist,'/user')
api.add_resource(Users,'/user/<user_id>')


if __name__ == '__main__':
    app.run()