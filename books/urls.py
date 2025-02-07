# urls.py
from django.urls import path
from .views import (
    BookListCreateView,
    BookDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    CommentListCreateView,
    CommentDetailView,
)

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path(
        "books/<int:book_id>/reviews/",
        ReviewListCreateView.as_view(),
        name="book-reviews",
    ),
    path(
        "books/<int:book_id>/reviews/<int:pk>/",
        ReviewDetailView.as_view(),
        name="review-detail",
    ),
    path(
        "books/<int:book_id>/comments/",
        CommentListCreateView.as_view(),
        name="book-comments",
    ),
    path(
        "books/<int:book_id>/comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]
