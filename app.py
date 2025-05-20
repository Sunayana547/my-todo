from flask import Flask, render_template,request,redirect # Added render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sunnu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    

    def __repr__(self):
        return f"{self.title} {self.desc}"  




@app.route('/hello', methods=['GET', 'POST'])
def helloworld():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)  # ✅ Save to database
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)



@app.route('/show')
def hello():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'Hello, World!'


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect("/hello")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
