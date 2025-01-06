from django.db import models
from django.contrib.auth.models import User

class DreamVacation(models.Model):
    CATEGORY_CHOICES = [
        ('Beach', 'Beach'),
        ('Hiking', 'Hiking'),
        ('Cottage', 'Cottage'),
        ('Cruise', 'Cruise'),
        ('Others', 'Others'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='vacation_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def interaction_score(self):
        comments = self.comments.all()
        return sum([comment.upvotes.count() for comment in comments]) + len(comments)

class Comment(models.Model):
    vacation = models.ForeignKey(DreamVacation, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=1)
    text = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_upvotes(self):
        return self.upvotes.count()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.vacation.title}'
