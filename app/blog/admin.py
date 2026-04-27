from flask_ckeditor import CKEditorField

from app.admin.views import MyBaseModelView


class BlogPostView(MyBaseModelView):
    column_list = ('title', 'slug', 'is_published', 'views_count', 'created_at')
    column_sortable_list = ('title', 'created_at', 'is_published', 'views_count')
    form_overrides = {'content': CKEditorField}
    form_excluded_columns = ('created_at', 'updated_at', 'views_count', 'reactions', 'comments')


class BlogTagView(MyBaseModelView):
    column_list = ('name', 'slug')


class CommentView(MyBaseModelView):
    column_list = ('post', 'user', 'content', 'created_at')
    column_sortable_list = ('created_at',)
    form_excluded_columns = ('created_at',)
    can_create = False
