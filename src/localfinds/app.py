from flask import Flask, render_template, request, redirect, url_for, session
import jinja_partials
from src.localfinds.database.posts_db import initialize_posts_db, store_post, get_post, get_all_posts, clear_posts
from src.localfinds.database.accounts_db import initialize_accounts_db, store_account, get_account, get_account_by_username, update_account, delete_account, clear_accounts

accounts_db = "./data/accounts.db"
posts_db = "./data/posts.db"

app = Flask(__name__, template_folder="./templates")
app.secret_key = 'localfindsprivatekey'
jinja_partials.register_extensions(app)

# ------------Initialize Database------------
initialize_accounts_db(accounts_db)
initialize_posts_db(posts_db)

clear_accounts(accounts_db)
clear_posts(posts_db) 

store_account(
    accounts_db,
    "admin",
    "password"
)
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
    return render_template("home/index.html", posts=posts)

@app.route("/post/<int:post_id>")
def serve_post(post_id):
    post = get_post(posts_db, post_id)
    if post:
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
        author_id = session["username"]

        store_post(
            posts_db,
            subject,
            content,
            author_id,
            address,
            tags
        )

        return redirect(url_for("home"))
    return render_template("home/create_post.html")

@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success = store_account(accounts_db, username, password)
        if not success:
            error = "Username is taken!"
            return render_template("home/create_account.html", error=error)

        account = get_account_by_username(accounts_db, username)

        if account and account["password"] == password:
            session["user_id"] = account["id"]
            session["username"] = account["username"]
        return redirect(url_for("home"))
    
    return render_template("home/create_account.html", error = error)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        account = get_account_by_username(accounts_db, username)

        if account and account["password"] == password:
            session["user_id"] = account["id"]
            session["username"] = account["username"]
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials!"

    return render_template("home/login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ------------Run App------------

if __name__ == "__main__":
    app.run(debug=True)