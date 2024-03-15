#pip install flask
#pip install flask_restful
from flask import Flask
from flask_restful import Resource, Api,reqparse,abort
#pip install flask_mysqldb
from flask_mysqldb import MySQL

app=Flask(__name__)
api=Api(app)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="vine96"
app.config["MYSQL_DB"]="db4b10"

mysql=MySQL(app)


Items={
    101:{"pname":"BMW", "price":500000.00},
    102:{"pname":"AUDI", "price":600000.00},
    103:{"pname":"MERC", "price":700000.00},
}

task_post=reqparse.RequestParser()
task_post.add_argument("pname", type=str, help="Enter pname", required=True)
task_post.add_argument("price", type=float, help="Enter price", required=True)

task_put=reqparse.RequestParser()
task_put.add_argument("pname", type=str)
task_put.add_argument("price", type=float)

class Product(Resource):
    def get(self, pid):
        return Items[pid]

    # def post(self, pid):
    #     args=task_post.parse_args()
    #     if pid in Items:
    #         abort(409, "Pid is already exist")
    #
    #     Items[pid]={"pname": args["pname"], "price": args["price"]}
    #     return Items[pid]

    def post(self, pid):
        args=task_post.parse_args()

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO products VALUES(%s,%s,%s)",(pid, args["pname"], args["price"]))
        mysql.connection.commit()

        return "record inserted successfully"


    def put(self, pid):
        args=task_put.parse_args()
        if pid not in Items:
            abort(404,"pid is not available")

        if args["pname"]:
            Items[pid]["pname"]=args["pname"]

        if args["price"]:
            Items[pid]["price"]=args["price"]
            # Items[101]["price"]="AUDI"
        return Items[pid]

    def delete(self, pid):
        del Items[pid]
        return Items
class AllProducts(Resource):
    def get(self):
        return Items


api.add_resource(Product, "/product/<int:pid>")
api.add_resource(AllProducts, "/product")

if __name__=="__main__":
    app.run(debug=True)