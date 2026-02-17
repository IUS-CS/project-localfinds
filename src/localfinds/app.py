from flask import Flask, render_template, request, redirect, url_for
from database.posts_db import initialize_db, store_post, get_post, get_all_posts, clear_posts, posts_db

app = Flask(__name__, template_folder="./templates")

# ------------Initialize Database------------
initialize_db(posts_db)
clear_posts(posts_db) 
store_post(
    posts_db,
    "Welcome to LocalFinds!",
    "This is the first post. Feel free to explore and create your own posts!",
    "admin",
    "123 Main St, Anytown, USA",
    "welcome, intro"
)

# ------------Routes------------

@app.route("/")
def home():
    posts = get_all_posts(posts_db) 
    return render_template("index.html", posts=posts)

@app.route("/post/<int:post_id>")
def serve_post(post_id):
    post = get_post(posts_db, post_id)
    if post:
        return render_template("view_post.html", post=post)
    else:
        return "Post not found", 404
    
@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]
        address = request.form["address"]
        tags = request.form["tags"]
        author_id = request.form["author_id"]

        store_post(
            posts_db,
            subject,
            content,
            author_id,
            address,
            tags
        )

        return redirect(url_for("home"))

    return render_template("create_post.html")

# ------------Run App------------

if __name__ == "__main__":
    app.run(debug=True)