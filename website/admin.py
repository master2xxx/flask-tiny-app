from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Post
from werkzeug.security import generate_password_hash
from . import db
from flask_login import login_required, current_user

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have access to the admin panel.', category='error')
        return redirect(url_for('views.home'))
        
    users = User.query.all()
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template("admin.html", user=current_user, users=users, posts=posts)

@admin.route('/toggle-block/<int:user_id>', methods=['POST'])
@login_required
def toggle_block(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Unauthorized access'})
        
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'success': False, 'error': 'User not found'})
        
    # Don't allow blocking of other admins
    if target_user.is_admin and target_user.id != current_user.id:
        return jsonify({'success': False, 'error': 'Cannot block admin users'})
        
    target_user.is_blocked = not target_user.is_blocked
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'is_blocked': target_user.is_blocked,
        'message': f'User {"blocked" if target_user.is_blocked else "unblocked"} successfully'
    })

@admin.route('/reset-password/<int:user_id>', methods=['POST'])
@login_required
def reset_password(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Unauthorized access'})
        
    target_user = User.query.get(user_id)
    if not target_user:
        return jsonify({'success': False, 'error': 'User not found'})
    
    # Set default password as "Password123"
    default_password = "Password123"
    target_user.password = generate_password_hash(default_password, method='pbkdf2:sha256')
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Password reset to "{default_password}" successfully'
    })

@admin.route('/delete-post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Unauthorized access'})
        
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'success': False, 'error': 'Post not found'})
    
    db.session.delete(post)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Post deleted successfully'
    })