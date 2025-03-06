from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Post
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Get 5 most recent posts
    recent_posts = Post.query.order_by(Post.date_created.desc()).limit(5).all()
    return render_template("home.html", user=current_user, posts=recent_posts)

@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("notes.html", user=current_user, notes=user_notes)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})