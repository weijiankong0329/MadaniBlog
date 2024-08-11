from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Blogger
from .models import Post
from .models import Comment
from .models import Category
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)

class BloggerInline(admin.StackedInline):
    model = Blogger
    can_delete = False
    verbose_name_plural = "blogger"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [BloggerInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
