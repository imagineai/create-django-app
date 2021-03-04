import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory
from todoapp.serializers import CommentSerializer

from .factories import CommentFactory


class CommentSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.comment = CommentFactory.create()

    def test_that_a_comment_is_correctly_serialized(self):
        comment = self.comment
        serializer = CommentSerializer
        serialized_comment = serializer(comment).data

        assert serialized_comment['id'] == comment.id
        assert serialized_comment['message'] == comment.message
        assert serialized_comment['status'] == comment.status
        assert serialized_comment['submitted'] == str(comment.submitted)
