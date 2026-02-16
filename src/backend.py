from flask import Flask, jsonify, render_template
from database.posts_db import initialize_db, create_post, get_post, get_all_posts, clear_posts, posts_db

app = Flask(__name__, template_folder="./templates")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_all_posts", methods=["GET"])
def serve_all_posts():
    posts = get_all_posts(posts_db)
    return jsonify(posts)
    
@app.route("/get_post/<int:post_id>", methods=["GET"])
def serve_post(post_id):
    post = get_post(posts_db, post_id)
    if post:
        return jsonify(dict(post))
    else:
        return jsonify({"error": "Post not found"}), 404
    
if __name__ == "__main__":
    initialize_db(posts_db)
    clear_posts(posts_db) 
    create_post(posts_db, "Welcome to LocalFinds!", "This is the second post. Feel free to explore and create your own posts!", "admin", "N/A", "welcome, intro")
    app.run(debug=True)
