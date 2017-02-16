用flask-restful 提供webserver
把数据库查询的结果 以json的格式发送出来
测试
curl http://127.0.0.1:5000/user
<result>
[
  {
    "id": 2,
    "username": "jk1156"
  }
]
</result>