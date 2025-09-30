from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
# Create your models here.

class Petition(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending REVIEW'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('implemented', 'Movie Added'),

    ]

    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length = 300,
        help_text = "Movie title you want to create a petition for"
    )

    description = models.TextField(
        validators=[MinLengthValidator(50)],
        help_text = "Why should this movie be added?"

    )
    movie_year = models.IntegerField(
        null = True,
        blank = True,
        help_text = "Release year"

    )
    director = models.CharField(
        max_length=100,
        blank = True,
        help_text = "Director name (optional)"

    )

    genre = models.CharField(
        max_length=50,
        blank = True,
        help_text = "Movie genre optional"

    )

    imdb_link = models.URLField(
        blank = True,
        help_text = "IMDB link optional"

    )

    created_by = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        related_name = 'created_petitions'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = 'pending'
    )

    admin_notes = models.TextField(
        blank = True,
        help_text="Admin notes"
    )

    def get_vote_count(self):
        return self.votes.count()
    def get_upvote_count(self):
        return self.votes.filter(vote_type='up').count()
    def get_downvote_count(self):
        return self.votes.filter(vote_type='down').count()

    
class Meta:
    ordering = ['-created_at']
    unique_together = ['title', 'movie_year']
    
    def _str_(self):
        return f"{self.title} ({self.movie_year or 'Unknown Year'})"

    def get_vote_count(self):
        return self.votes.count()


class Vote(models.Model):
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]

    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(
    Petition,
    on_delete=models.CASCADE,
    related_name = 'votes'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='petition_votes'
    )

    vote_type = models.CharField(max_length=4, choices = VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ['petition', 'user']
    ordering = ['-created_at']

    
    def _str_(self):
        return f"{self.user.username} - {self.get_vote_type_display()} - {self.petition.title}"



