from rest_framework import serializers
from .models import Book, Review, Comment


class BookSerializer(serializers.ModelSerializer):
    publisher = serializers.StringRelatedField(read_only=True)
    review_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'publisher', 'review_count', 'comment_count']
        read_only_fields = ['publisher']

    def get_review_count(self, obj):
        return obj.book_reviews.count()

    def get_comment_count(self, obj):
        return obj.book_comments.count()

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate_description(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "book", "user", "rating", "content", "created_at", "updated_at"]
        read_only_fields = ["user", "book"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "book", "user", "content", "created_at", "updated_at"]
        read_only_fields = ["user", "book"]
