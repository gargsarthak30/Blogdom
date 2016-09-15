# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-15 08:47
from __future__ import unicode_literals

import blogs.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=150)),
                ('blog_content', models.TextField()),
                ('upvotes', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=blogs.models.content_post_image)),
            ],
        ),
        migrations.CreateModel(
            name='UpvoteDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upvoted', models.BooleanField(default=False)),
                ('postid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Post')),
            ],
        ),
        migrations.CreateModel(
            name='UserBlogdom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100)])),
                ('bio', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=blogs.models.content_profile_picture)),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to=blogs.models.content_cover_picture)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='upvotedetail',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.UserBlogdom'),
        ),
        migrations.AddField(
            model_name='post',
            name='blogger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.UserBlogdom'),
        ),
    ]
