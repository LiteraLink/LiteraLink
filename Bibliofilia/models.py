from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from authentication.models import UserBook

# Create your models here.
class Forum (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    BookName = models.CharField(max_length=255)
    userbook = models.ForeignKey(UserBook, on_delete=models.SET_NULL, null=True, blank=True)
    forumsDescription = models.CharField(max_length=255)
    bookPicture = models.ImageField(upload_to='reviewimages/')
    userReview = models.TextField(blank=True, null=True)
    repliesTotal = models.IntegerField()
    dateOfPosting = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.BookName  # Or any other meaningful representation

class ForumReply(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    pictureReplies = models.ImageField(upload_to='reviewimages/')
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Reply to {self.forum.BookName} by {self.username}'
    
    def formatted_timestamp(self):
        return self.timestamp.strftime("%d-%m-%y")


class Message(models.Model):
    sender = models.ForeignKey(Forum, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} sent at {self.timestamp}'