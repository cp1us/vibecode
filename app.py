# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request
import flask_login
from flask_login import current_user

from sqlalchemy import select, update, delete
from data import *
from forms import *
import flask_migrate

import config
from log import logger

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["LOGIN_DISABLED"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URL

login_manager = flask_login.LoginManager(app)
db = db_init(app)
migrate = flask_migrate.Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get_one(User, user_id)
    return user


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


def get_notices():
    if not current_user.is_authenticated:
        return []
    notices = db.session.scalars(
        select(Notice).where(Notice.op_id == current_user.id).order_by(Notice.date.desc()).limit(4)
    )
    return notices.all()


@app.route("/")
@app.route("/index")
def index():
    page = request.args.get('page', 1, type=int)

    query = select(Post).order_by(Post.date.desc())
    posts = db.paginate(query, page=page, per_page=10, error_out=False)

    return render_template("index.html",
                           title="Форум",
                           user=current_user,
                           posts=posts,
                           notices=get_notices())


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")

    reg_form = RegisterForm()
    params = {"title": "Регистрация",
              "form": reg_form,
              "user": current_user,
              "notices": get_notices()}

    if reg_form.validate_on_submit():
        result = db.session.execute(
            select(User.email).where(User.email == reg_form.email.data)
        )
        mail = result.scalar_one_or_none()
        if mail:
            print("Регистрация: была введена некорректная почта")
            logger.debug("Регистрация: была введена некорректная почта")
            return render_template("register.html",
                                   **params,
                                   redalert="Данный email уже используется")
        result = db.session.execute(
            select(User.username).where(User.username == reg_form.username.data)
        )
        username = result.scalar_one_or_none()
        if username:
            print("Регистрация: такое имя пользователя уже существует")
            logger.debug("Регистрация: такое имя пользователя уже существует")
            return render_template("register.html",
                                   **params,
                                   redalert="Данное имя пользователя уже используется")

        if reg_form.passwd.data != reg_form.passwd_repeat.data:
            print("Регистрация: пароли не совпадают")
            logger.debug("Регистрация: пароли не совпадают")
            return render_template("register.html",
                                   **params,
                                   redalert="Пароли не совпадают")

        passwd_valid = User.validate_password(reg_form.passwd.data)
        username_valid = User.validate_username(reg_form.username.data)
        if passwd_valid and username_valid:
            new_user = User(email=reg_form.email.data,
                            username=reg_form.username.data)
            new_user.set_password(reg_form.passwd.data)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"Регистация пользователя {new_user.username}, email: {new_user.email}")

            return redirect("/login")
        if not username_valid:
            print("Регистрация: было введено неверное имя пользователя")
            logger.debug("Регистрация: было введено неверное имя пользователя")
            return render_template("register.html",
                                   **params,
                                   redalert="Неверное имя пользователя: разрешены латинские буквы, цифры и _")
        if not passwd_valid:
            print("Регистрация: был введен неверный пароль")
            logger.debug("Регистрация: был введен неверный пароль")
            return render_template("register.html",
                                   **params,
                                   redalert="Неверный пароль: разрешены латинские буквы, цифры и !@#$%^&*_+=")

    return render_template("register.html", **params)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    log_form = LoginForm()
    params = {"title": "Авторизация",
              "form": log_form,
              "user": current_user,
              "notices": get_notices()}

    if log_form.validate_on_submit():
        result = db.session.execute(
            select(User).where(User.email == log_form.email.data)
        )
        user: User = result.scalar()

        if user and user.check_password(log_form.passwd.data):
            flask_login.login_user(user, remember=log_form.remember_me.data)
            logger.debug(f"Вход пользователя {user.username}, email: {user.email}")
            return redirect("/")

        logger.debug("Регистрация: был введен неверный логин или пароль")
        return render_template('login.html',
                               **params,
                               redalert="Неверный логин и/или пароль")

    return render_template("login.html", **params)


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/profile/<string:username>")
def profile(username: str):
    result = db.session.execute(
        select(User).where(User.username == username)
    )
    user: User = result.scalar_one_or_none()

    if user:
        return render_template("profile.html",
                               profile=user,
                               title=user.username,
                               user=current_user,
                               notices=get_notices())

    return "<h1>404</h1>"


@app.route("/profile")
@flask_login.login_required
def current_profile():
    return redirect(f"/profile/{current_user.username}")


@app.route("/post/<int:identify>", methods=["GET", "POST"])
def post(identify: int):
    comment_form = CommentForm()
    result = db.session.execute(
        select(Post).where(Post.id == identify)
    )
    post: Post = result.scalar_one_or_none()
    if post:
        if current_user.is_authenticated and post.op_id == current_user.id:
            db.session.execute(
                delete(Notice).where(Notice.post_id == post.id and Notice.op_id == current_user.id)
            )
        if comment_form.validate_on_submit() and current_user.is_authenticated:
            comment = Comment(post_id=post.id,
                              op_id=current_user.id,
                              op_username=current_user.username,
                              text=comment_form.text.data)
            db.session.add(comment)
            db.session.execute(
                update(User).where(User.id == current_user.id).values(total_comments=current_user.total_comments + 1)
            )
            db.session.commit()

            if post.op_id != current_user.id:
                notice = Notice(
                    op_id=post.op_id,
                    post_id=post.id,
                    post_header=post.header,
                    sender_username=current_user.username
                )
                db.session.add(notice)
                db.session.commit()

        page = request.args.get('page', 1, type=int)
        query = select(Comment).where(Comment.post_id == post.id).order_by(Comment.date)
        comments = db.paginate(query, page=page, per_page=20, error_out=False)

        params = {"title": post.header,
                  "form": comment_form,
                  "user": current_user,
                  "post": post,
                  "comments": comments,
                  "notices": get_notices()}

        return render_template("post.html",
                               **params)

    return "<h1>404</h1>"


@app.route("/post/<int:identify>/delete")
@flask_login.login_required
def post_delete(identify: int):
    result = db.session.execute(
        select(Post).where(Post.id == identify)
    )
    post: Post = result.scalar_one_or_none()
    if post and post.op_id == current_user.id:
        db.session.execute(
            delete(Post).where(Post.id == identify)
        )
        db.session.execute(
            delete(Comment).where(Comment.post_id == identify)
        )
        db.session.commit()

        return redirect("/")

    return redirect(f"/post/{identify}")


@app.route("/post/<int:post_identify>/comment_del/<int:comment_identify>")
@flask_login.login_required
def comment_delete(post_identify: int, comment_identify: int):
    result = db.session.execute(
        select(Comment).where(Comment.id == comment_identify)
    )
    comment: Comment = result.scalar_one_or_none()
    if comment and comment.op_id == current_user.id:
        db.session.execute(
            delete(Comment).where(Comment.id == comment_identify)
        )
        db.session.commit()

    return redirect(f"/post/{post_identify}")


@app.route("/posts")
@flask_login.login_required
def user_posts():
    page = request.args.get('page', 1, type=int)

    query = select(Post).where(Post.op_id == current_user.id).order_by(Post.date.desc())
    posts = db.paginate(query, page=page, per_page=20, error_out=False)

    return render_template("index.html",
                           title=f"Ваши посты",
                           user=current_user,
                           posts=posts,
                           notices=get_notices())


@app.route("/create", methods=["GET", "POST"])
@flask_login.login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            op_username=current_user.username,
            op_id=current_user.id,
            header=form.header.data,
            text=form.text.data
        )
        db.session.add(post)
        db.session.flush()
        db.session.execute(
            update(User).where(User.id == current_user.id).values(total_posts=current_user.total_posts + 1)
        )
        db.session.commit()
        logger.debug(f"Создан новый пост: {post.header}")
        return redirect(f"post/{post.id}")
    return render_template("create_post.html",
                           title="Создание поста",
                           form=form,
                           user=current_user,
                           notices=get_notices())


@app.route("/search/<string:search>")
def searching(search: str):
    page = request.args.get('page', 1, type=int)

    query = select(Post).where(Post.header.like(f"%{search}%")).order_by(Post.date.desc())
    posts = db.paginate(query, page=page, per_page=20, error_out=False)

    return render_template("index.html",
                           title=f"Запрос: {search}",
                           user=current_user,
                           posts=posts,
                           notices=get_notices())


@app.route("/notifications")
@flask_login.login_required
def notifications():
    page = request.args.get('page', 1, type=int)

    query = select(Notice).where(Notice.op_id == current_user.id).order_by(Notice.date.desc())
    notices = db.paginate(query, page=page, per_page=40, error_out=False)

    return render_template("notifications.html",
                           title=f"Уведомления",
                           user=current_user,
                           notifications=notices)


@app.route("/notifications/clear")
@flask_login.login_required
def clear_notifications():
    db.session.execute(
        delete(Notice).where(Notice.op_id == current_user.id)
    )
    db.session.commit()
    return redirect("/notifications")


def main():
    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == "__main__":
    main()
