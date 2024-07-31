from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from yuli.auth import login_required
from yuli.db import get_db

bp = Blueprint("blog", __name__)


@login_required
@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    note = None
    if g.user:
        note = db.execute("SELECT * FROM notes WHERE author_id is {}".format( \
                g.user['id'])).fetchone()
    return render_template("portal/dashboard.html", note=note)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))


@bp.route("/leads", methods=("GET", "POST"))
@login_required
def leads_index():
    """List view of leads."""
    sort_by = request.args.get('sort_by')
    order = request.args.get('order', default='ASC')

    sql_query = None
    form_data = request.form
    if form_data.__len__() > 0:
        search_query = form_data['search_query']
        try:
            search_query = int(search_query)
        except ValueError:
            search_query = "'%{}%'".format(search_query)
        sql_query = "WHERE {} {} {}".format(
            form_data['search_by'],
            form_data['search_operation'],
            search_query
        )

    db = get_db()
    leads = db.execute(
        "SELECT * FROM leads {} ORDER BY {} {}".format(
            "" if not sql_query else sql_query,
            sort_by if sort_by else 'zip',
            order
        )
    ).fetchall()
    return render_template("blog/leads.html",
                           leads=leads,
                           sort_by=sort_by,
                           order=order)


@bp.route("/leads/<int:id>")
@login_required
def leads_view(id):
    """Singleton view of a lead."""
    db = get_db()
    lead = db.execute("SELECT * FROM leads WHERE id is {}".format(id)) \
        .fetchone()
    return render_template("blog/lead.html", lead=lead)


@bp.route("/edit_notes", methods=("GET", "POST"))
@login_required
def edit_notes():
    """Form to edit a user's personal notes."""
    db = get_db()
    note = db.execute("SELECT * FROM notes WHERE author_id is {}".format(g.user['id'])) \
            .fetchone()

    if request.method == "POST":
        body = request.form["body"]

        error = False
        try:
            if not note.body: #note exists
                error = True
        except:
            error = True

        if not error:
            db.execute("UPDATE notes SET body = ? WHERE author_id = ?",
                (body, g.user['id'])
            )
            db.commit()
        else: #note doesn't exist
            db.execute(
                "INSERT INTO notes (body, author_id) VALUES (?, ?)",
                (body, g.user["id"]),
            )
            db.commit()


        return redirect(url_for('blog.index'))

    return render_template("portal/notes.html", note=note)
