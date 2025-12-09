from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
