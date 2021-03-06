from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User


class UserBlogdom(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MaxValueValidator(100)])
    bio = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)
    cover_picture = models.ImageField(blank=True, null = True)

    User.profile = property(lambda u: UserBlogdom.objects.get_or_create(user=u)[0])

    def __str__(self):
        desc = self.user.username
        return desc

    def count_upvotes(self):
        total_upvotes = self.post_set.all().aggregate(Sum('upvotes'))
        return total_upvotes

    def count_posts(self):
        total_posts = self.post_set.all().count()
        return total_posts

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})

    def get_rating(self):
        upvotes = self.count_upvotes().get('upvotes__sum')
        posts = self.count_posts()
        if upvotes is None:
            upvotes = 0
        rating = float((((upvotes * 0.75) + (posts * 0.25))/2))
        return rating


class Post(models.Model):
    blogger = models.ForeignKey(UserBlogdom, on_delete=models.CASCADE)
    heading = models.CharField(max_length=150)
    blog_content = models.TextField()
    upvotes = models.IntegerField(default=0)
    time = models.DateTimeField(editable=False, default=timezone.localtime(timezone.now()))
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.heading

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.blogger})


class UpvoteDetail(models.Model):
    postid = models.ForeignKey(Post, on_delete=models.CASCADE)
    userid = models.ForeignKey(UserBlogdom, on_delete=models.CASCADE)
    upvoted = models.BooleanField(default=False)

