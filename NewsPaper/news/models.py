from django.db import models
from .resources import POSTNEWS_CATEGORIES
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username.title()}: {self.rating}'


    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating_news'), 0))['pr']
        comments_rating = Comment.objects.filter(comment_user=self.user).aggregate(cr=Coalesce(Sum('rating_comment'), 0))['cr']
        post_comments_rating = Comment.objects.filter(comment_post__author=self).aggregate(pcr=Coalesce(Sum('rating_comment'), 0))['pcr']
        self.rating = (posts_rating*3) + comments_rating + post_comments_rating
        self.save()

        print(f' Рейтинг постов  - {posts_rating}, \n '
              f'Рейтинг комментариев автора - {comments_rating}, \n'
              f' Рейтинг комментариев постов автора - {post_comments_rating}, \n'
              f' Общий рейтинг - {self.rating} ')


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    post_news = models.CharField(max_length=20, choices=POSTNEWS_CATEGORIES, default='POST')    #поле с выбором статья/новость
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating_news = models.IntegerField(default=0)

    def like_post(self):
        self.rating_news += 1
        self.save()

    def dislike_post(self):
        self.rating_news -= 1
        self.save()

    def preview_post(self):
        preview = self.content[:124] + '...'
        return preview


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    time_in_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like_comment(self):
        self.rating_comment += 1
        self.save()

    def dislike_comment(self):
        self.rating_comment -= 1
        self.save()

