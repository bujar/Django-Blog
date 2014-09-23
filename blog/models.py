from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=50)

#    following = models.CharField(max_length=30)
    def __str__(self):
		return self.user

# main user list used to keep track of registered users
# this will cause redundancy but I didn't want to modify the Item model
class userList(models.Model):
	username = models.CharField(max_length=30)
	follows = models.CharField(max_length=30)
	def __str__(self):
		return self.username

class followList(models.Model):
	username = models.CharField(max_length=30)
	follows = models.CharField(max_length=30)
	def __str__(self):
		return self.follows

class blogPost(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	username = models.CharField(max_length=30)
	text = models.CharField(max_length=160)
	title = models.CharField(max_length=30)
	picture = models.ImageField(upload_to='blog-photos', blank=True)
	def __str__(self):
		return self.text

