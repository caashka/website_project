from flask import Flask, render_template
from database import db
from tasks import tasks
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.bd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(tasks)


@app.route('/')
def root():
    return render_template("root.html")


if __name__ == "__main__":
    app.run(debug=True)
