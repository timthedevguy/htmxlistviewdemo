from django.db import models
from django.utils import timezone

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField()
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    @property
    def age(self):
        return timezone.now().year - self.date_of_birth.year