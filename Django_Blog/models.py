from django.db import models


AUTH_USER_MODEL = 'django_facebook.FacebookCustomUser'
AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'



class user(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
class posts(models.Model):
    name=models.CharField(max_length=200)
    post=models.CharField(max_length=200)
    pl=models.CharField(max_length=200)
    comment=models.CharField(max_length=200)
    cn=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
class comments(models.Model):
    post=models.CharField(max_length=200)
    com=models.CharField(max_length=200)
    date=models.CharField(max_length=200)




    
