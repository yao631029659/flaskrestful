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

# 控制显示的字段
post_fileds={
    'id':fields.Integer,
    'username':fields.String
}
class Userlist(Resource):
    # 把数据查询json化
    @marshal_with(post_fileds)
    def get(self):
        user=User.query.all()
        return user

    def post(self):
        if not request.json:
            print('没有回传数据')
            abort(400)
        print('回传的数据是')
        print(request.json['username'])
        #  request.json回传的数据是字典
        user=User(username=request.json['username'])
        print(request.json)
        db.session.add(user)
        db.session.commit()

# 删除和修改都必须使用带url参数的
class Users(Resource):
    def delete(self,user_id):
        print('删除被调用')
        print('user_id',user_id)
        # print(request.json) request 用json是收不到值的
        user=User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()

    def put(self,user_id):
        print('修改被调用')
        print('user_id',user_id)
        print(request.json)
        user=User.query.filter_by(id=user_id).first()
        user.username=request.json['username']
        db.session.commit()



## Actually setup the Api resource routing here
##
api.add_resource(Userlist,'/user')
api.add_resource(Users,'/user/<user_id>')


if __name__ == '__main__':
    app.run()