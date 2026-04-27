from flask import render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required

from app.extensions import db
from app.blog import blueprint
from app.blog.models import BlogPost, BlogTag, PostReaction, Comment
from app.blog.forms import CommentForm


@blueprint.route('/')
def index():
    posts = (BlogPost.query
             .filter_by(is_published=True)
             .order_by(BlogPost.created_at.desc())
             .all())
    tags = BlogTag.query.order_by(BlogTag.name).all()
    return render_template('blog/index.html', posts=posts, tags=tags)


@blueprint.route('/tag/<slug>')
def by_tag(slug):
    tag = BlogTag.query.filter_by(slug=slug).first_or_404()
    posts = (BlogPost.query
             .filter(BlogPost.tags.contains(tag), BlogPost.is_published == True)
             .order_by(BlogPost.created_at.desc())
             .all())
    tags = BlogTag.query.order_by(BlogTag.name).all()
    return render_template('blog/index.html', posts=posts, tags=tags, current_tag=tag)


@blueprint.route('/<slug>')
def post(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    post.views_count = (post.views_count or 0) + 1
    db.session.commit()
    return render_template(
        'blog/post.html',
        post=post,
        user_reaction=post.user_reaction(current_user),
        comment_form=CommentForm(),
    )


@blueprint.route('/<slug>/react/<action>', methods=['POST'])
@login_required
def react(slug, action):
    if action not in ('like', 'dislike'):
        abort(400)
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    is_like = action == 'like'
    reaction = PostReaction.query.filter_by(post_id=post.id, user_id=current_user.id).first()
    if reaction is None:
        db.session.add(PostReaction(post_id=post.id, user_id=current_user.id, is_like=is_like))
    elif reaction.is_like == is_like:
        db.session.delete(reaction)
    else:
        reaction.is_like = is_like
    db.session.commit()
    return redirect(url_for('blog.post', slug=slug) + '#reactions')


@blueprint.route('/<slug>/comment', methods=['POST'])
@login_required
def add_comment(slug):
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()
    form = CommentForm(request.form)
    if form.validate():
        db.session.add(Comment(post_id=post.id, user_id=current_user.id, content=form.content.data.strip()))
        db.session.commit()
    return redirect(url_for('blog.post', slug=slug) + '#comments')


@blueprint.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id and not getattr(current_user, 'is_admin', False):
        abort(403)
    slug = comment.post.slug
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('blog.post', slug=slug) + '#comments')
