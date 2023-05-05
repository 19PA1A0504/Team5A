from django.db import models

# Create your models here.
from django.db.models import CASCADE


class Userregister_Model(models.Model):
    name= models.CharField(max_length=50)
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=10)
    phoneno=models.CharField(max_length=15)
    address=models.CharField(max_length=500)
    dob=models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    status = models.CharField(max_length=30,default=0)

class TweetModel(models.Model):
    userId = models.ForeignKey(Userregister_Model,on_delete=CASCADE )
    tweet = models.CharField(max_length=500)
    topics = models.CharField(max_length=300)
    sentiment = models.CharField(max_length=300)
    status = models.CharField(max_length=300,default=0)
    images = models.FileField()

class Feedback_Model(models.Model):
    name = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100)
    feedback = models.CharField(max_length=300)
