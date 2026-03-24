from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import jinja_partials
from src.localfinds.database.posts_db import initialize_posts_db, store_post, get_post, get_all_posts, clear_posts, update_post, delete_post
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
    generate_password_hash("password")
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

@app.route("/posts/create", methods=["GET", "POST"])
def create_post():
    if "username" not in session:
        return "Unauthorized", 403
    
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

@app.route("/")
def home():
    posts = get_all_posts(posts_db) 
    return render_template("home/index.html", posts=posts)

@app.route("/posts/<int:post_id>")
def serve_post(post_id):
    post = get_post(posts_db, post_id)
    if post:
        return render_template("home/view_post.html", post=post)
    else:
        return "Post not found", 404

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = get_post(posts_db, post_id)
    if not post:
        return "Post not found", 404
    
    if "username" not in session or session["username"] != post["author_id"]:
        return "Unauthorized", 403  

    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]
        address = request.form["address"]
        tags = request.form["tags"]

        update_post(posts_db, post_id, subject, content, address, tags)

        return redirect(url_for("serve_post", post_id=post_id))

    return render_template("home/edit_post.html", post=post)

@app.route("/posts/<int:post_id>/delete")
def remove_post(post_id):
    post = get_post(posts_db, post_id)
    if not post:
        return "Post not found", 404

    if "username" not in session or session["username"] != post["author_id"]:
        return "Unauthorized", 403

    delete_post(posts_db, post_id)
    return redirect(url_for("home"))

@app.route("/accounts/create", methods=["GET", "POST"])
def create_account():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)

        success = store_account(accounts_db, username, password_hash)
        if not success:
            error = "Username is taken!"
            return render_template("home/create_account.html", error=error)

        account = get_account_by_username(accounts_db, username)

        if account and check_password_hash(account["password"], password):
            session["user_id"] = account["id"]
            session["username"] = account["username"]
        return redirect(url_for("home"))
    
    return render_template("home/create_account.html", error = error)

@app.route("/accounts/<string:username>")
def view_account(username):
    account = get_account_by_username(accounts_db, username)
    if account:
        return render_template("home/view_account.html", account=account)
    else:
        return "Account not found", 404

@app.route("/accounts/<string:username>/edit", methods=["GET", "POST"])
def edit_account(username):
    account = get_account_by_username(accounts_db, username)
    if not account:
        return "Account not found", 404

    if "user_id" not in session or (session["user_id"] != account["id"] and session["username"] != "admin"):
        return "Unauthorized", 403
    
    if request.method == "POST":
        username = request.form["username"]

        existing_account = get_account_by_username(accounts_db, username)
        if existing_account and existing_account["id"] != account["id"]:
            return "Username already taken", 400

        password = request.form["password"]
        password_hash = generate_password_hash(password)

        update_account(accounts_db, account["id"], username, password_hash)
        session["username"] = username
        
        return redirect(url_for("view_account", username=username))

    return render_template("home/edit_account.html", account=account)

@app.route("/accounts/<string:username>/delete", methods=["GET", "POST"])
def remove_account(username):
    account = get_account_by_username(accounts_db, username)
    if not account:
        return "Account not found", 404

    if "user_id" not in session or (session["user_id"] != account["id"] and session["username"] != "admin"):
        return "Unauthorized", 403

    delete_account(accounts_db, account["id"])

    if session["user_id"] == account["id"]:
        session.clear()

    return redirect(url_for("home"))

@app.route("/auth/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        account = get_account_by_username(accounts_db, username)

        if account and check_password_hash(account["password"], password):
            session["user_id"] = account["id"]
            session["username"] = account["username"]
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials!"

    return render_template("home/login.html", error=error)

@app.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ------------Run App------------

if __name__ == "__main__":
    app.run(debug=True)