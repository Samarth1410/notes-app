from flask import Blueprint,flash, render_template, request, jsonify #bunch of urls
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from website.models import Note
from website import db
import json

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note is too short", category="error")
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")

    return render_template("home.html", user = current_user)
    
#Delete note receive delete note request->send note.id to JS -> JS transfer request to delete-note
@views.route('/delete-note', methods= ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
