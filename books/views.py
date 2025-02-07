from rest_framework import generics
from .models import Book, Review, Comment
from .serializers import BookSerializer, ReviewSerializer, CommentSerializer
from .paginations import BookPagination, ReviewPagination, CommentPagination
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBookPublisherOrReadOnly, IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import ValidationError


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            if not self.request.data.get('title'):
                raise ValidationError({"detail": "Title is required."})
            if not self.request.data.get('description'):
                raise ValidationError({"detail": "Description is required."})
            if not self.request.data.get('author'):
                raise ValidationError({"detail": "Author is required."})

            if Book.objects.filter(
                title=self.request.data['title'],
                author=self.request.data['author']
            ).exists():
                raise ValidationError({
                    "detail": "A book with this title and author already exists."
                })

            serializer.save(publisher=self.request.user)

        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError({
                "detail": f"An error occurred while creating the book: {str(e)}"
            })


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsBookPublisherOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(publisher=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ReviewPagination

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs.get("book_id"))

    def perform_create(self, serializer):
        try:
            book = Book.objects.get(id=self.kwargs.get("book_id"))
        except Book.DoesNotExist:
            raise ValidationError({"detail": "Book does not exist."})

        if book.publisher == self.request.user:
            raise ValidationError({"detail": "You cannot review your own book."})
        serializer.save(user=self.request.user, book=book)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs.get("book_id"))


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination

    def get_queryset(self):
        return Comment.objects.filter(book_id=self.kwargs.get("book_id"))

    def perform_create(self, serializer):
        try:
            book = Book.objects.get(id=self.kwargs.get("book_id"))
        except Book.DoesNotExist:
            raise ValidationError({"detail": "Book does not exist."})

        if book.publisher == self.request.user:
            raise ValidationError({"detail": "You cannot comment on your own book."})
        serializer.save(user=self.request.user, book=book)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(book_id=self.kwargs.get("book_id"))
