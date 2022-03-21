from flask import Blueprint, request, flash
from flask import Flask, render_template, redirect, url_for
from .forms import BlogForm, BlogCommentForm
from blogapp.models import Blog, BlogComment
from blogapp import db
from sqlalchemy.exc import IntegrityError
from flask_login import login_required

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    blog_form = BlogForm(request.form)
    if blog_form.validate_on_submit():
        blog = Blog(title=blog_form.title.data, content=blog_form.content.data)
        try:
            db.session.add(blog)
            db.session.commit()
            flash(f"You have posted a blog!")
        except InterruptedError:
            db.session.rollback()
            flash(f"Error, unable to post a blog")
            return redirect(url_for('blog.index'))
        return redirect(url_for('blog.allblogs'))
    return render_template('index.html', form=blog_form)


@blog_bp.route('/all')
@login_required
def allblogs():
    return render_template('blogs.html', query=Blog.query.all())


@blog_bp.route('/all/<title>')
@login_required
def blog_delete(title):
    blog = Blog.query.get(title)
    if blog is None:
        flash(f"Error, the blog might not exist", 'error')
        return redirect(url_for('blog.allblogs'))
    try:
        db.session.delete(blog)
        db.session.commit()
    except InterruptedError:
        db.session.rollback()
        flash(f"Error, unable to delete the blog", "error")
        return redirect(url_for('blog.allblogs'))
    return redirect(url_for('blog.allblogs'))


@blog_bp.route('/blogs/<title>', methods=['GET', 'POST'])
@login_required
def view_blog_by_id(title):
    comment_form = BlogCommentForm()
    blog = Blog.query.filter_by(title=title).first()
    if blog is None:
        flash(f"Error, the blog might not exist", 'error')
        return redirect(url_for('blog.allblogs'))
    else:
        content = blog.content
        if comment_form.validate_on_submit():
            comment = BlogComment(blog_title=title, content=comment_form.comment.data)
            try:
                db.session.add(comment)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                flash(f'Error, unable to post a comment. ', 'error')
                return redirect(url_for('blog.view_by_blog_id', title=title, form=comment_form))

            comments = BlogComment.query.filter_by(blog_title=title).all()
            return render_template('blog.html', title=title, content=content, comments=comments, form=comment_form)

        comments = BlogComment.query.filter_by(blog_title=title).all()
        return render_template('blog.html', title=title, content=content, comments=comments, form=comment_form)
