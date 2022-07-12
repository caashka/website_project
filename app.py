from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_from = db.Column(db.Integer)
    user_to = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Tasks %r' % self.id


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    file = db.Column(db.LargeBinary)

    def __repr__(self):
        return '<Files %r' % self.id

@app.route('/')
def root():
    return render_template("root.html")


@app.route('/tasks')
def tasks():
    tasks = Tasks.query.order_by(Tasks.date)
    files = Files.query.order_by(Files.task_id)
    return render_template("tasks.html", tasks=tasks, files=files)


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        files = request.files.getlist('file')
        task = Tasks(title=title, text=text, user_to=1, user_from=1)
        for file in files:
            print(file)
            add = Files(task_id=1, file=file.read())
            try:
                db.session.add(add)
                db.session.commit()
            except:
                print('ошибка в файлах')
                return redirect('/tasks')
        try:
            db.session.add(task)
            db.session.commit()
        except:
            print('ошибка в таске')
            return redirect('/tasks')
        return render_template("create.html")
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
