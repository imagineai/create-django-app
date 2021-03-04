import json

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Comment
from .factories import CommentFactory, TodoFactory
from .utils import generate_authenticated_api_client, generate_user

faker = Factory.create()


class Comment_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        CommentFactory.create_batch(size=3)
        self.todo = TodoFactory.create()
        management.call_command("initialize")
        self.authenticated_api_client = generate_authenticated_api_client(
            generate_user(
                permissions=[]
            )
        )

    def test_create_comment(self):
        """
        Ensure we can create a new comment object.
        """
        client = self.authenticated_api_client
        comment_count = Comment.objects.count()
        comment_dict = factory.build(dict, FACTORY_CLASS=CommentFactory, todo=self.todo.pk)
        response = client.post(reverse('comment-list'), comment_dict)
        created_comment_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Comment.objects.count() == comment_count + 1
        comment = Comment.objects.get(pk=created_comment_pk)

        assert comment_dict['submitted'] == str(comment.submitted)

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.authenticated_api_client
        response = client.get(reverse('comment-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Comment.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.authenticated_api_client
        comment_qs = Comment.objects.all()
        comment_count = Comment.objects.count()

        for i, comment in enumerate(comment_qs, start=1):
            response = client.delete(reverse('comment-detail', kwargs={'pk': comment.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert comment_count - i == Comment.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.authenticated_api_client
        comment_pk = Comment.objects.first().pk
        comment_detail_url = reverse('comment-detail', kwargs={'pk': comment_pk})
        comment_dict = factory.build(dict, FACTORY_CLASS=CommentFactory, todo=self.todo.pk)
        response = client.patch(comment_detail_url, data=comment_dict)
        assert response.status_code == status.HTTP_200_OK

        assert comment_dict['message'] == response.data['message']
        assert comment_dict['submitted'] == response.data['submitted']
        assert comment_dict['status'] == response.data['status']

    def test_update_submitted_with_incorrect_value_data_type(self):
        client = self.authenticated_api_client
        comment = Comment.objects.first()
        comment_detail_url = reverse('comment-detail', kwargs={'pk': comment.pk})
        comment_submitted = comment.submitted
        data = {
            'submitted': faker.pystr(),
        }
        response = client.patch(comment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert comment_submitted == Comment.objects.first().submitted

    def test_update_message_with_incorrect_value_outside_constraints(self):
        client = self.authenticated_api_client
        comment = Comment.objects.first()
        comment_detail_url = reverse('comment-detail', kwargs={'pk': comment.pk})
        comment_message = comment.message
        data = {
            'message': faker.pystr(min_chars=513, max_chars=513),
        }
        response = client.patch(comment_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert comment_message == Comment.objects.first().message
