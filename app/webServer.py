from flask import Flask,Blueprint, render_template, request
from functions.configManager import config, parent_dir
import sqlite3
from datetime import datetime

views=Blueprint("views",__name__)
config=config()

app=Flask(__name__)

@views.route("/test")
def test():
    return render_template("test.html")

@views.route("/")
def main():
    config.load()
    data=config.data
    treshold_price=data["treshold_price"]
    con_type=data["plug"]["connection"]

    with open(f"{parent_dir}app/data/output.log","r") as f:
        logs=f.read().splitlines()


    timestamp=datetime.now().replace(minute=0,second=0, microsecond=0).timestamp()

    conn=sqlite3.connect(f"{parent_dir}app/data/cenas.sqlite")
    c=conn.cursor()
    c.execute(f"SELECT price FROM main WHERE timestamp={timestamp};")
    rows = c.fetchall()
    conn.close()

    cur_price=rows[0][0]

    return render_template("main.html",treshold_price=treshold_price,con_type=con_type,logs=logs,cur_price=cur_price)

@views.route("/change/treshold_price",methods=["POST"])
def updateTP():
    new_tresh_price=float(request.json["treshold_price"])
    print(new_tresh_price)
    config.load()
    config.data["treshold_price"]=new_tresh_price
    config.update()
    return "Be happy!"

app.register_blueprint(views,url_prefix="/")
app.run(debug=True)




