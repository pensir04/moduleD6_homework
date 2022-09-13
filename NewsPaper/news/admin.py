from django.contrib import admin
from .models import Author, Post, Category, PostCategory, Comment, Subscriber

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Категории'''
    list_display = ('id', 'categories', 'get_subscribers')

    def get_subscribers(self, obj):
        return "\n".join([s.username for s in obj.subscribers.all()])

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    '''Новость или статья'''
    list_display = ('id', 'selection', 'postAuthor', 'get_category', 'time', 'header', 'text', 'rating')
    list_display_links = ('id', 'header',)

    # for ManyToManyField fields we create a custom method and add that method's name to list_display
    # OR define a model method and use that, see the comments in class Post file models.py
    def get_category(self, obj):
        return "\n".join([cat.categories for cat in obj.postCategory.all()])


admin.site.register(Subscriber)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
