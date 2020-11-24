from django.db import models
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post_pic = models.ImageField(null=True, blank=True, upload_to='post_pic')
	likes = models.ManyToManyField(User, related_name='blog_post')

	def total_likes(self):
		return self.likes.count()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('detail', args=[str(self.id)])

	
class Comment(models.Model):
	post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
	body = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	authors = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


	class Meta:
		ordering = ['-date_added']
        

	
	def __str__(self):
		return '%s' % (self.post.title + " " +"comments")

	