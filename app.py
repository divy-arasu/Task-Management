from flask import Flask, render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db= SQLAlchemy(app)

class Mytask(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    content=db.Column(db.String(100), nullable = False)
    complete=db.Column(db.Integer, default = 0)
    created=db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"
@app.route("/", methods=["POST","GET"])
def index():
    #add task
    if request.method == "POST":
        current_task=request.form["content"]
        new_task = Mytask(content = current_task)
        try :
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR {e}"
        
    else:
        task = Mytask.query.order_by(Mytask.created).all()
        return render_template("index.html",tasks=task)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Mytask.query.get(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROE {e}"
    
@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id : int):
    cur_task = Mytask.query.get(id)
    if request.method == "POST":
        cur_task.content=request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR{e}"
    else:
        return render_template("update.html",task=cur_task)
    

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
