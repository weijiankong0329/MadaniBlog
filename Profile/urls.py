from django.urls import path
from . import views

urlpatterns = [
    path("<slug:slug>/", views.BloggerDetailView.as_view(), name="profile"),
    path("edit/<slug:slug>/", views.BloggerUpdateView.as_view(), name="edit-profile")
]
