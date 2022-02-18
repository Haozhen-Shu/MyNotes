from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import User, db, Notebook, Note
from app.forms import NotebookForm, NoteForm

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
# @login_required
def users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
# @login_required
def user(id):
    user = User.query.get(id)
    return user.to_dict()


@user_routes.route('/<int:userid>/notebooks')
# @login_required
def get_all_notebooks(userid):
    all_notebooks = Notebook.query.filter_by(userid=userid).all()
    return {"notebooks": [notebook.to_dict() for notebook in all_notebooks]}


@user_routes.route('/<int:userid>/notebooks/<int:notebookid>')
# @login_required
def get_one_notebook(userid, notebookid):
    notebook = Notebook.query.filter_by(userid=userid, id=notebookid).first()
    notes = Note.query.filter_by(notebookid=notebookid).all()
    return {"notebook": notebook.to_dict(), "notes": [note.to_dict() for note in notes]}

@user_routes.route('/<int:userid>/notebooks', methods=["POST"])
# @login_required
def create_one_notebook(userid):
    form = NotebookForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    form["userid"].data = userid
    print(form['title'], "TTTTTTTTTitle")
    print(form.data, "Datatattaatat")
    if form.validate_on_submit()and form.title_valid():
        data = request.get_json()
        notebook = Notebook(userid = userid,
                            title = data['title']
        )
        db.session.add(notebook)
        db.session.commit()
        all_notebooks = Notebook.query.filter_by(userid=userid).all()
        return {"notebook": notebook.to_dict(), "notebooks":[notebook.to_dict() for notebook in all_notebooks]}
    else:
        return jsonify({"errors": form.errors})
#         # jsonify serializes data to JavaScript Object Notation (JSON) format

@user_routes.route('/<int:userid>/notebooks/<int:notebookid>', methods=["PATCH"])
# @login_required
def edit_one_notebook(userid, notebookid):
    form  = NotebookForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    form["userid"].data = userid
    if form.validate_on_submit() and form.title_valid():
        data = request.get_json()
        notebook = Notebook.query.get(notebookid)
        if "title" in data.keys() and data["title"] != "":
            notebook.title = data["title"]
        db.session.commit()
        all_notebooks = Notebook.query.filter_by(userid=userid).all()
        return {"notebooks": [notebook.to_dict() for notebook in all_notebooks]}
    else:
        return jsonify({"errors": form.errors})

@user_routes.route('/<int:userid>/notebooks/<int:notebookid>', methods=["DELETE"])
# @login_required
def remove_one_notebook(userid, notebookid):
    notebook = Notebook.query.filter_by(id=notebookid).first()
    db.session.delete(notebook)
    db.session.commit()
    all_notebooks = Notebook.query.filter_by(userid=userid).all()
    return {"notebooks": [notebook.to_dict() for notebook in all_notebooks]}
