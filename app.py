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


app.config['MAX_FILESIZE'] = 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['PNG', 'JPEG', 'JPG', 'DOCX', 'PDF']


def allowed_file_size(filesize):
    if int(filesize) <= app.config['MAX_FILESIZE']:
        return True
    else:
        return False


def allowed_extensions(filename):
    if not'.' in filename:
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.upper() in app.config['ALLOWED_EXTENSIONS']:
        return True
    else:
        return False


@app.route('/create', methods=['GET', 'POST'])
def create_task():
    if request.method == "POST":
        print(request.cookies)

        title = request.form['title']
        text = request.form['text']
        files = request.files.getlist('file')
        task = Tasks(title=title, text=text, user_to=1, user_from=1)
        if request.method == "POST":
            print(request.cookies)
            if not allowed_file_size(request.cookies.get('filesize')):
                print('file too big')
                return redirect('/create')
        try:
            db.session.add(task)
            db.session.commit()
        except:
            print('ошибка в таске')
            return redirect('/tasks')

        for file in files:

            if not allowed_extensions(file.filename):
                print('неверное расширение')
                return redirect('/create')

            add = Files(task_id=task.id, file=file.read())

            try:
                db.session.add(add)
                db.session.commit()
            except:
                print('ошибка в файлах')
                return redirect('/tasks')

        return render_template("create.html")
    else:
        return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)
