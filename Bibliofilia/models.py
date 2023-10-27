from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Forum (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    BookName = models.CharField(max_length=255)
    forumsDescription = models.CharField(max_length=255)
    bookPicture = models.ImageField(upload_to='reviewimages/')
    userReview = models.TextField()
    dateOfPosting = models.DateField(auto_now_add=True)

class ForumReply(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    text = models.TextField()
    pictureReplies = models.ImageField(upload_to='reviewimages/')
    timestamp = models.DateTimeField(default=timezone.now)

class Message(models.Model):
    sender = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} sent at {self.timestamp}'