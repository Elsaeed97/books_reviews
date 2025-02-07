from django.contrib import admin
from .models import Book, Review, Comment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'created_at')
    list_filter = ('publisher', 'created_at')
    search_fields = ('title', 'author', 'publisher__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('book', 'user', 'created_at')
    search_fields = ('book__title', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at')
    list_filter = ('book', 'user', 'created_at')
    search_fields = ('book__title', 'user__username')
