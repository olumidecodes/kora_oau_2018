from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Ajo_Group_Details(models.Model):
    ajo_code = models.CharField(unique=True, max_length=4)
    contributors = models.ManyToManyField(User)
    money_to_be_contributed = models.IntegerField(default=0)
    contributors_payed = models.ManyToManyField(User, related_name='+')


class User_Dashboard_Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ajo_groups = models.ManyToManyField(Ajo_Group_Details)


def UserDashboardCreate(sender, **kwargs):
    if kwargs['created']:
        User_Dashboard_Details.objects.create(user=kwargs['instance'])

post_save.connect(UserDashboardCreate, sender=User)

class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_code = models.CharField(max_length=10)
    amount = models.IntegerField()
    status = models.BooleanField(default=False)

