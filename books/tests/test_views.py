from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Book, Review, Comment

User = get_user_model()


class BookViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='otheruser@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.book_data = {
            "title": "Test Book",
            "description": "Test Description",
            "author": "Test Author",
        }

        self.book = Book.objects.create(
            title="Existing Book",
            description="Existing Description",
            author="Existing Author",
            publisher=self.user,
        )

    def test_create_book(self):
        url = reverse('book-list')
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest('id').publisher, self.user)

    def test_create_duplicate_book(self):
        url = reverse('book-list')
        # Create first book
        self.client.post(url, self.book_data)
        # Try to create duplicate
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.id})
        updated_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "author": "Updated Author",
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.publisher = User.objects.create_user(
            username='publisher',
            password='testpass123',
            email='publisher@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            description="Test Description",
            author="Test Author",
            publisher=self.publisher,
        )

        self.review_data = {
            'rating': 5,
            'content': 'Great book!',
            'book': self.book.id
        }

    def test_create_review(self):
        url = reverse('book-reviews', kwargs={'book_id': self.book.id})
        response = self.client.post(url, self.review_data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Review creation failed with error: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_publisher_cannot_review_own_book(self):
        self.client.force_authenticate(user=self.publisher)
        url = reverse('book-reviews', kwargs={'book_id': self.book.id})
        response = self.client.post(url, self.review_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.publisher = User.objects.create_user(
            username='publisher',
            password='testpass123',
            email='publisher@example.com'
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            description="Test Description",
            author="Test Author",
            publisher=self.publisher,
        )

        self.comment_data = {
            'content': 'Test comment',
            'book': self.book.id
        }

    def test_create_comment(self):
        url = reverse('book-comments', kwargs={'book_id': self.book.id})
        response = self.client.post(url, self.comment_data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Comment creation failed with error: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_publisher_cannot_comment_own_book(self):
        self.client.force_authenticate(user=self.publisher)
        url = reverse('book-comments', kwargs={'book_id': self.book.id})
        response = self.client.post(url, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
