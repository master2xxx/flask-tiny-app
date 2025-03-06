from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post
from . import db

posts = Blueprint('posts', __name__)

@posts.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    if current_user.is_blocked:
        flash('Your account is blocked. You cannot create posts.', category='error')
        return redirect(url_for('views.home'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content cannot be empty', category='error')
        else:
            new_post = Post(title=title, content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', category='success')
            return redirect(url_for('posts.list_posts'))
            
    return render_template('create_post.html', user=current_user)

@posts.route('/posts')
def list_posts():
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('posts.html', user=current_user, posts=posts)

@posts.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_post.html', user=current_user, post=post)

@posts.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # Check if user is blocked
    if current_user.is_blocked and not current_user.is_admin:
        flash('Your account is blocked. You cannot edit posts.', category='error')
        return redirect(url_for('posts.view_post', post_id=post_id))
        
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author or an admin
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this post.', category='error')
        return redirect(url_for('posts.view_post', post_id=post_id))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Title and content cannot be empty', category='error')
        else:
            post.title = title
            post.content = content
            db.session.commit()
            flash('Post updated successfully!', category='success')
            return redirect(url_for('posts.view_post', post_id=post_id))
            
    return render_template('edit_post.html', user=current_user, post=post)

@posts.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Check if the current user is the author or an admin
    if post.user_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this post.', category='error')
        return redirect(url_for('posts.view_post', post_id=post_id))
        
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', category='success')
    return redirect(url_for('posts.list_posts'))