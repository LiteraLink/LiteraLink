from django.test import TestCase
from .models import Forum, ForumReply, Message
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class ForumModelTest(TestCase):
    def test_forum_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        forum = Forum.objects.create(
            user=user,
            BookName='Test Book',
            forumsDescription='Description',
            userReview='User Review',
            repliesTotal=0,
            dateOfPosting=timezone.now(),
            username='testuser'
        )
        self.assertIsInstance(forum, Forum)
        self.assertEqual(forum.__str__(), 'Test Book')

class ForumReplyModelTest(TestCase):
    def test_forum_reply_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        forum = Forum.objects.create(
            user=user,
            BookName='Test Book',
            forumsDescription='Description',
            userReview='User Review',
            repliesTotal=0,
            dateOfPosting=timezone.now(),
            username='testuser'
        )
        forum_reply = ForumReply.objects.create(
            forum=forum,
            user=user,
            username='testuser',
            text='Test Reply',
            timestamp=timezone.now()
        )
        self.assertIsInstance(forum_reply, ForumReply)
        self.assertEqual(forum_reply.__str__(), 'Reply to Test Book by testuser')

class MessageModelTest(TestCase):
    def test_message_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        forum = Forum.objects.create(
            user=user,
            BookName='Test Book',
            forumsDescription='Description',
            userReview='User Review',
            repliesTotal=0,
            dateOfPosting=timezone.now(),
            username='testuser'
        )
        message = Message.objects.create(
            sender=forum,
            content='Test Message',
            timestamp=timezone.now()
        )
        self.assertIsInstance(message, Message)
        self.assertEqual(message.__str__(), f'Message from {forum} sent at {message.timestamp}')
