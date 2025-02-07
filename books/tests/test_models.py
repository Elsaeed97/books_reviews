from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from books.models import Book, Review, Comment

User = get_user_model()


class BookModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            publisher=self.user,
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.description, "Test Description")
        self.assertEqual(self.book.publisher, self.user)

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Test Book")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.publisher = User.objects.create_user(
            username="publisher", email="publisher@example.com", password="testpass123"
        )
        self.reviewer = User.objects.create_user(
            username="reviewer", email="reviewer@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            publisher=self.publisher,
        )

    def test_review_creation(self):
        review = Review.objects.create(
            book=self.book, user=self.reviewer, rating=5, content="Great book!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.content, "Great book!")
        self.assertEqual(review.user, self.reviewer)

    def test_review_str_method(self):
        review = Review.objects.create(
            book=self.book, user=self.reviewer, rating=5, content="Great book!"
        )
        expected_str = f"Review by {self.reviewer.username} on {self.book.title}"
        self.assertEqual(str(review), expected_str)

    def test_invalid_rating(self):
        review = Review(
            book=self.book,
            user=self.reviewer,
            rating=6,  # Invalid rating > 5
            content="Great book!",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_publisher_cannot_review_own_book(self):
        with self.assertRaises(ValidationError):
            Review.objects.create(
                book=self.book,
                user=self.publisher,  # Publisher trying to review their own book
                rating=5,
                content="Great book!",
            )

    def test_unique_review_per_user_per_book(self):
        Review.objects.create(
            book=self.book, user=self.reviewer, rating=5, content="Great book!"
        )

        duplicate_review = Review(
            book=self.book,
            user=self.reviewer,  # Same user trying to review same book again
            rating=4,
            content="Changed my mind",
        )

        with self.assertRaises(ValidationError):
            duplicate_review.full_clean()


class CommentModelTest(TestCase):
    def setUp(self):
        self.publisher = User.objects.create_user(
            username="publisher", email="publisher@example.com", password="testpass123"
        )
        self.commenter = User.objects.create_user(
            username="commenter", email="commenter@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            publisher=self.publisher,
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            book=self.book, user=self.commenter, content="Great book!"
        )
        self.assertEqual(comment.content, "Great book!")
        self.assertEqual(comment.user, self.commenter)

    def test_comment_str_method(self):
        comment = Comment.objects.create(
            book=self.book, user=self.commenter, content="Great book!"
        )
        expected_str = f"Comment by {self.commenter.username} on {self.book.title}"
        self.assertEqual(str(comment), expected_str)

    def test_publisher_cannot_comment_on_own_book(self):
        with self.assertRaises(ValidationError):
            Comment.objects.create(
                book=self.book,
                user=self.publisher,  # Publisher trying to comment on their own book
                content="Great book",
            )
