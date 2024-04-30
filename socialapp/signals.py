from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from django.contrib.auth import get_user_model
User = get_user_model()


@receiver(m2m_changed, sender=Post.likes.through)
def total_likes_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


