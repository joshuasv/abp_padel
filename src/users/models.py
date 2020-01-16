import re

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from PIL import Image

class User(AbstractUser):
    SEX_CHOICES = [('M', 'Male'), ('F', 'Female')]
    email = models.EmailField(blank=False, unique=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    dni = models.CharField(max_length=9, unique=True)
    socio = models.BooleanField(default=False)
    

    def clean(self, *args, **kwargs):
        if not self.validate_dni(self.dni):
            raise ValidationError({'dni': _('DNI or NIF incorrect format.')})
        super(User, self).clean(*args, **kwargs)

    def validate_dni(self, value):
        value = value.upper()
        nif_regex = r"^[0-9]{8}[TRWAGMYFPDXBNJZSQVHLCKE]$"
        nie_regex = r"^[XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$"
        return re.match(nif_regex, value) or re.match(nie_regex, value)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
