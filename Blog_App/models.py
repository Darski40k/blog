from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField(max_length=255, verbose_name='Write a Title')
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(verbose_name='What do you think about that..?')
    image = models.ImageField(upload_to='blog_images', verbose_name='Put image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.comment


class Likes(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
