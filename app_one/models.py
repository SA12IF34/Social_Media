from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    
    account_name = models.CharField(max_length=65)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    followers_number = models.DecimalField(max_digits=8, decimal_places=0, default=0, blank=False)
    followers_accounts = models.ManyToManyField('Follow', blank=True)

    def __str__(self):

        return f"{self.account_name}"

class Follow(models.Model):
    name = models.CharField(max_length=150)
    account_name = models.CharField(max_length=150)
    email = models.EmailField()
    follow_accounts = models.ManyToManyField(Account, blank=True)


# ----------------------------------------------------------------------------------------------------------------------


def upload_to(self, filename):
    return '{name}/{filename}'.format(filename=filename, name=self.author.name)

class Post(models.Model):
    
    desc = models.CharField(max_length=500)
    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False, null=True)
    likes = models.DecimalField(max_digits=5, decimal_places=0, default=0, blank=True)
    shares = models.DecimalField(max_digits=5, decimal_places=0, default=0, blank=False)
    file = models.FileField(upload_to=upload_to ,blank=True, null=True) # JsonField

class Comment(models.Model):
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=800, default="hello")



    
 