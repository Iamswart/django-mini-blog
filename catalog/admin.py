from django.contrib import admin
from .models import Author, Category, Blogpost, Comment
# Register your models here.

# admin.site.register(Author)
admin.site.register(Category)
# admin.site.register(Blogpost)
admin.site.register(Comment)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'picture')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_category')
    list_filter = ('author', 'category')
    inlines = [CommentInline]
        


    
        

