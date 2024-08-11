from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('list/', views.BlogPostList.as_view(),name='view'),
    path('list/<int:pk>', views.BlogPostOther,name='viewOther'),
    path('manage/', views.ManagePostList.as_view(),name='manage'),
    path('add/', views.AddPostView.as_view(),name='add'),
    path('post/<slug:slug>/', views.PostCommentDetailView.as_view(),name='postDetail'),
    path('post/edit/<slug:slug>/', views.editPostView.as_view(), name='postEdit'),
    path('post/delete/<slug:slug>/', views.deletePostView, name='postDelete'),
    path('loginregister/', views.LoginRegisterView.as_view(),name='loginregister'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'),
        name='passwordReset'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('createEditBlog/', views.AddBlogView.as_view(),name='createEditBlog'),
    path('fav/<int:pk>/', views.favView, name='fav')
]