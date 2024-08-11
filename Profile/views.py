from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView
from Home.models import Blogger
from .forms import UserForm, BloggerForm
from django.http import HttpResponseRedirect

# Create your views here.


class BloggerDetailView(DetailView):
    model = Blogger
    template_name = "Profile/profile.html"
    context_object_name = "blogger"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogger = self.get_object()
        followers = blogger.follower.all()
        following = blogger.following_users.all()
        fav_posts = blogger.fav_post.all()
        context["blogger_user"] = blogger.user
        context["blogger_followers"] = followers
        context["blogger_followings"] = following
        context["fav_posts"] = fav_posts
        return context

    def post(self, request, *args, **kwargs):
        if (request.user.is_anonymous):
            return HttpResponseRedirect(reverse('Personal:loginregister'))
        else:
            blogger = self.get_object()
            user = blogger.user
            current_blogger = request.user.blogger

            if "follow" in request.POST:
                current_blogger.following_users.add(user)
                user.blogger.follower.add(request.user)
            elif "unfollow" in request.POST:
                current_blogger.following_users.remove(user)
                user.blogger.follower.remove(request.user)

            return redirect("Profile:profile", slug=blogger.slug)


class BloggerUpdateView(LoginRequiredMixin, UpdateView):
    model = Blogger
    template_name = "Profile/edit-profile.html"
    form_class = BloggerForm

    def get_success_url(self):
        blogger = self.object
        return reverse("Profile:profile", kwargs={"slug": blogger.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_form" not in context:
            context["user_form"] = UserForm(instance=self.object.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user_form = UserForm(request.POST, instance=self.object.user)
        blogger_form = self.get_form()
        if user_form.is_valid() and blogger_form.is_valid():
            return self.form_valid(user_form, blogger_form)
        else:
            return self.form_invalid(user_form, blogger_form)

    def form_valid(self, user_form, blogger_form):
        user_form.save()
        blogger_form.save()
        return super().form_valid(blogger_form)

    def form_invalid(self, user_form, blogger_form):
        return self.render_to_response(
            self.get_context_data(user_form=user_form, form=blogger_form)
        )
