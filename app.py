from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, User
import os
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics=PrometheusMetrics(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route("/users/add", methods=["POST"])
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")
    if name and email:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/users/<int:user_id>/update", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.name = request.form.get("name", user.name)
    user.email = request.form.get("email", user.email)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")  
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(host=host, port=port)
