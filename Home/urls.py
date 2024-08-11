from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="home"),
    path('post/<int:pk>/', views.PostCommentDetailView.as_view(), name='post_detail'),
    path('tag/<int:tag_id>/', views.tag_posts, name='tag_posts'),
    path('search/', views.search, name='search'),
    path('fav/<int:pk>/',views.favView,name='fav')
]