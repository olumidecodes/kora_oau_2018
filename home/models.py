from django.db import models
from django.contrib.auth.models import User

class Ajo_Group_Details(models.Model):
    ajo_code = models.CharField(unique=True, max_length=4)
    contributors = models.ManyToManyField(User)
    money_to_be_contributed = models.IntegerField(default=0)


class User_Dashboard_Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ajo_groups = models.ManyToManyField(Ajo_Group_Details)


