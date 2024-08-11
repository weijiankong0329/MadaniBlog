from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify


def user_directory_path(instance, filename):
    if isinstance(instance, Post):
        return "user_{0}/posts/{1}".format(instance.author.id, filename)
    elif isinstance(instance, Blogger):
        return "user_{0}/bloggers/{1}".format(instance.user.id, filename)


class Category(models.Model):
    label_category = models.CharField(max_length=20)

    def __str__(self):
        return self.label_category


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    creation_datetime = models.DateTimeField(auto_now=True)
    modification_datetime = models.DateTimeField(default=datetime.now, blank=True)
    slug = models.SlugField(default='null',null=True,blank=True)
    category = models.ManyToManyField(Category,default='null')


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.modification_datetime = datetime.now()
        self.slug = '%i-%i-%s' % (
            self.author.id,self.id,slugify(self.title[0:45])
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    blogger = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comment_user",
        default="null",
        blank=True,
        null=True,
    )
    published_date = models.DateTimeField(auto_now=True)


class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_image = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
    )
    tagline = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    # social links
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    website_link = models.URLField(blank=True)

    # blog info
    blog_title = models.CharField(max_length=500, blank=True, null=True)
    blog_description = models.TextField(blank=True)
    blog_image = models.ImageField(upload_to=user_directory_path, blank=True)

    following_users = models.ManyToManyField(
        User, related_name="following_user", default="null", null=True, blank=True
    )
    follower = models.ManyToManyField(
        User, related_name="follower", default="null", null=True, blank=True
    )
    fav_post = models.ManyToManyField(Post, default="null", null=True, blank=True)
    slug = models.SlugField(default="null", null=False, unique=True)

    def user__username(self):
        return self.user.name

    def get_absolute_url(self):
        return reverse("Profile:profile", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.get_username())
        return super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Blogger.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.blogger.save()
