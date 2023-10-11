from django.db import models

class Book(models.Model):
    kind = models.CharField(max_length=255)
    google_id = models.CharField(max_length=255)  # Rename 'id' field to 'google_id' or another suitable name
    etag = models.CharField(max_length=255)
    selfLink = models.URLField()
    title = models.CharField(max_length=255)
    authors = models.TextField()
    publisher = models.CharField(max_length=255)
    publishedDate = models.DateField()
    description = models.TextField()
    textReadingMode = models.BooleanField()
    imageReadingMode = models.BooleanField()
    pageCount = models.PositiveIntegerField()
    printType = models.CharField(max_length=255)
    categories = models.TextField()
    maturityRating = models.CharField(max_length=255)
    allowAnonLogging = models.BooleanField()
    contentVersion = models.CharField(max_length=255)
    containsEpubBubbles = models.BooleanField()
    containsImageBubbles = models.BooleanField()
    smallThumbnail = models.URLField()
    thumbnail = models.URLField()
    language = models.CharField(max_length=255)
    previewLink = models.URLField()
    infoLink = models.URLField()
    canonicalVolumeLink = models.URLField()

    def __str__(self):
        return self.title
