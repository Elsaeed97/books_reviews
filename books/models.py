from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    author = models.CharField(max_length=200, verbose_name=_('Author'))
    description = models.TextField(verbose_name=_('Description'))
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True, verbose_name=_('Cover Image'))
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='published_books', verbose_name=_('Publisher'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_reviews', verbose_name=_('Book'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews', verbose_name=_('User'))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Rating')
    )
    content = models.TextField(verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    class Meta:
        unique_together = ('book', 'user')

    def clean(self):
        if self.book.publisher == self.user:
            raise ValidationError("You cannot review your own book.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Review by {self.user.username} on {self.book.title}'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments', verbose_name=_('Book'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name=_('User'))
    content = models.TextField(verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))

    def clean(self):
        if self.book.publisher == self.user:
            raise ValidationError("You cannot comment on your own book.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'