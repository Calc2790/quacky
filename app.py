from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quacky.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(64), unique=True, nullable=False)
password = db.Column(db.String(128), nullable=False)
posts = db.relationship("Post", backref="user", lazy=True)

class Post(db.Model):
id = db.Column(db.Integer, primary_key=True)
user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
content = db.Column(db.String(256), nullable=False)
timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
likes = db.Column(db.Integer, default=0)

@app.route("/api/register", methods=["POST"])
def register():
username = request.json["username"]
password = bcrypt.generate_password_hash(request.json["password"]).decode("utf-8")
user = User(username=username, password=password)
db.session.add(user)
db.session.commit()
return jsonify({"message": "User created successfully"})

@app.route("/api/login", methods=["POST"])
def login():
username = request.json["username"]
password = request.json["password"]
user = User.query.filter_by(username=username).first()
if user and bcrypt.check_password_hash(user.password, password):
access_token = create_access_token(identity=user.id)
return jsonify({"access_token": access_token})
else:
return jsonify({"message": "Invalid username or password"}), 401

@app.route("/api/posts", methods=["POST"])
@jwt_required
def create_post():
user_id = get_jwt_identity()
content = request.json["content"]
post = Post(user_id=user_id, content=content)
db.session.add(post)
db.session.commit()
return jsonify({"message": "Post created successfully"})
@app.route("/api/posts/like", methods=["POST"])
@jwt_required
def like_post():
post_id = request.json["post_id"]
post = Post.query.get(post_id)
if post:
user_id = get_jwt_identity()
if post.user_id == user_id:
return jsonify({"message": "You cannot like your own post"}), 400
post.likes += 1
db.session.commit()
return jsonify({"message": "Post liked successfully"})
else:
return jsonify({"message": "Post not found"}), 404

@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
post = Post.query.get(post_id)
if post:
return jsonify({"content": post.content, "likes": post.likes})
else:
return jsonify({"message": "Post not found"}), 404

if __name__ == "__main__":
app.run(debug=True)
