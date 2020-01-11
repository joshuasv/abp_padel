from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail

from users.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

        # Get all emails
        emails = User.objects.values_list('email', flat=True)

        send_mail(
            'Noticias nuevas en iPadl!',
            'Se ha publicado una nueva noticia: ' + self.title + '\n\nLee más en http://127.0.0.1:8000' + self.get_absolute_url(),
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
