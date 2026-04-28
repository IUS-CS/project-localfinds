from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import jinja_partials
from src.localfinds.models.posts import (
    delete_all_posts_by_author,
    initialize_posts,
    store_post,
    get_post,
    get_all_posts,
    clear_posts,
    update_all_posts_author,
    update_post,
    delete_post,
    filter_posts,
)
from src.localfinds.models.accounts import (
    initialize_accounts,
    store_account,
    get_account,
    get_account_by_username,
    update_account,
    delete_account,
    clear_accounts,
)

accounts = "./data/accounts.db"
posts = "./data/posts.db"

app = Flask(__name__, template_folder="./templates")
app.secret_key = "localfindsprivatekey"
jinja_partials.register_extensions(app)

# ------------Initialize Database------------
initialize_accounts(accounts)
initialize_posts(posts)

clear_accounts(accounts)
clear_posts(posts)

store_account(accounts, "admin", generate_password_hash("password"))
store_post(
    posts,
    "Welcome to LocalFinds!",
    "This is the first post. Feel free to explore and create your own posts!",
    "admin",
    "123 Main St, Anytown, USA",
    "welcome, intro",
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

        store_post(posts, subject, content, author_id, address, tags)

        return redirect(url_for("home"))
    return render_template("home/create_post.html")


@app.route("/")
def home():
    all_posts = get_all_posts(posts)
    return render_template("home/index.html", all_posts=all_posts)


@app.route("/posts/search", methods=["GET", "POST"])
def search_posts():
    if request.method == "POST":
        search = request.form["search"]
        return redirect(url_for("search_posts", q=search))

    search = request.args.get("q", "")
    if search:
        results = filter_posts(posts, search)
    else:
        results = get_all_posts(posts)
    return render_template("home/index.html", all_posts=results, search=search)


@app.route("/posts/<int:post_id>")
def serve_post(post_id):
    post = get_post(posts, post_id)
    if post:
        return render_template("home/view_post.html", post=post)
    else:
        return "Post not found", 404


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = get_post(posts, post_id)
    if not post:
        return "Post not found", 404

    if "username" not in session or session["username"] != post["author_id"]:
        return "Unauthorized", 403

    if request.method == "POST":
        subject = request.form["subject"]
        content = request.form["content"]
        address = request.form["address"]
        tags = request.form["tags"]

        update_post(posts, post_id, subject, content, address, tags)

        return redirect(url_for("serve_post", post_id=post_id))

    return render_template("home/edit_post.html", post=post)


@app.route("/posts/<int:post_id>/delete")
def remove_post(post_id):
    post = get_post(posts, post_id)
    if not post:
        return "Post not found", 404

    if "username" not in session or (
        session["username"] != post["author_id"] and session["username"] != "admin"
    ):
        return "Unauthorized", 403

    delete_post(posts, post_id)
    return redirect(url_for("home"))


@app.route("/accounts/create", methods=["GET", "POST"])
def create_account():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 15:
            error = "Username must not exceed 15 characters"
            return render_template("home/create_account.html", error=error)

        password = request.form["password"]
        password_hash = generate_password_hash(password)

        success = store_account(accounts, username, password_hash)
        if not success:
            error = "Username is taken!"
            return render_template("home/create_account.html", error=error)

        account = get_account_by_username(accounts, username)

        if account and check_password_hash(account["password"], password):
            session["user_id"] = account["id"]
            session["username"] = account["username"]
        return redirect(url_for("home"))

    return render_template("home/create_account.html", error=error)


@app.route("/accounts/<string:username>")
def view_account(username):
    account = get_account_by_username(accounts, username)
    if account:
        return render_template("home/view_account.html", account=account)
    else:
        return "Account not found", 404


@app.route("/accounts/<string:username>/edit", methods=["GET", "POST"])
def edit_account(username):
    account = get_account_by_username(accounts, username)
    if username == "admin":
        return "Unable to modify adminstrator account", 403

    if not account:
        return "Account not found", 404

    if "user_id" not in session or (
        session["user_id"] != account["id"] and session["username"] != "admin"
    ):
        return "Unauthorized", 403

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 15:
            error = "Username must not exceed 15 characters"
            return render_template(
                "home/edit_account.html", error=error, account=account
            )

        existing_account = get_account_by_username(accounts, username)
        if existing_account and existing_account["id"] != account["id"]:
            return "Username already taken", 400

        password = request.form["password"]
        password_hash = generate_password_hash(password)

        bio = request.form.get("bio", "")

        update_all_posts_author(posts, account["username"], username)

        update_account(accounts, account["id"], username, password_hash, bio)
        session["username"] = username

        return redirect(url_for("view_account", username=username))

    return render_template("home/edit_account.html", account=account)


@app.route("/accounts/<string:username>/delete", methods=["GET", "POST"])
def remove_account(username):
    if username == "admin":
        return "Unable to delete adminstrator account", 403

    account = get_account_by_username(accounts, username)
    if not account:
        return "Account not found", 404

    if "user_id" not in session or (
        session["user_id"] != account["id"] and session["username"] != "admin"
    ):
        return "Unauthorized", 403

    delete_account(accounts, account["id"])
    delete_all_posts_by_author(posts, account["username"])

    if session["user_id"] == account["id"]:
        session.clear()

    return redirect(url_for("home"))


@app.route("/auth/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        account = get_account_by_username(accounts, username)

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
