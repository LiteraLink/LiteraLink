from django.db import models

class Book(models.Model):
    bookID = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.CharField(max_length=255)
    thumbnail = models.TextField()

    def __str__(self):
        return self.title
