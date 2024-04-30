from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from taggit.managers import TaggableManager


# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    photo = ResizedImageField(upload_to='media', blank=True, null=True, )
    bio = models.CharField(max_length=250, null=True, blank=True)
    following = models.ManyToManyField('self', through='Contact', related_name="followers", symmetrical=False)


class Post(models.Model):
    auther = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    caption = models.TextField()

    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    image = ResizedImageField(upload_to='media', blank=True, null=True)

    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    total_likes = models.PositiveIntegerField(default=0)
    saves = models.ManyToManyField(User, related_name="saved_posts", blank=True)

    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create']),
            models.Index(fields=['-total_likes']),
        ]

    def __str__(self):
        return self.auther.first_name

    def get_absolute_url(self):
        return self


class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    status = models.BooleanField(default=False)
    auther = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    create = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create']
        indexes = [
            models.Index(fields=['-create'])
        ]

    def __str__(self):
        return self.auther


class Ticket(models.Model):

    class Subject(models.TextChoices):
        CRITICISM = 'C', 'criticism'
        PROPOSAL = 'P', 'proposal'
        REPORT = 'R', ' report'

    subject = models.CharField(max_length=1, choices=Subject.choices)
    message = models.TextField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
