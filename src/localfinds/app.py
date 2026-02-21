from flask import Flask, render_template, request, redirect, url_for
import jinja_partials
from src.localfinds.database.posts_db import initialize_db, store_post, get_post, get_all_posts, clear_posts, posts_db

app = Flask(__name__, template_folder="./templates")
jinja_partials.register_extensions(app)

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
    # templates are organized under the "home" subdirectory
    return render_template("home/index.html", posts=posts)

@app.route("/post/<int:post_id>")
def serve_post(post_id):
    post = get_post(posts_db, post_id)
    if post:
        # view_post template resides in home subfolder
        return render_template("home/view_post.html", post=post)
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

    # create_post template is also inside the home directory
    return render_template("home/create_post.html")

# ------------Run App------------

if __name__ == "__main__":
    app.run(debug=True)