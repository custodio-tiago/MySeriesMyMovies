from django.contrib.auth.models import User
from django.db import models

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    title = models.CharField(max_length=255)
    movie_id = models.IntegerField()
    rating = models.FloatField(null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
