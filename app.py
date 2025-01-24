from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quacky.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

@app.route("/api/posts", methods=["POST"])
def create_post():
    user_id = request.json["user_id"]
    content = request.json["content"]
    post = Post(user_id=user_id, content=content)
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Post created successfully"})

if __name__ == "__main__":
    app.run(debug=True)
