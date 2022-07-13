from flask import Flask, render_template
from database import db
from tasks import tasks
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
max_filesize = 1024 * 1024
allowed_extensions = ['PNG', 'JPEG', 'JPG', 'DOCX', 'PDF']
db.init_app(app)
app.register_blueprint(tasks)


@app.route('/')
def root():
    return render_template("root.html")


if __name__ == "__main__":
    app.run(debug=True)
