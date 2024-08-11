from django import forms
from django.contrib.auth.models import User
from Home.models import Blogger


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class BloggerForm(forms.ModelForm):
    class Meta:
        model = Blogger
        fields = [
            "profile_image",
            "tagline",
            "bio",
            "twitter_link",
            "instagram_link",
            "facebook_link",
            "website_link",
        ]
