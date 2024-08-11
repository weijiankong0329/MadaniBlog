from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from .models import Post,Category
from django.contrib.auth.models import User
from .forms import BlogSearchForm
from PersonalBlog.forms import AddCommentsForm
from django.db.models import Q

def post_list(request):
    latest_posts = Post.objects.order_by('-creation_datetime')[:5]
    popular_posts = Post.objects.order_by('-modification_datetime')[:5]
    all_posts = Post.objects.all()
    tag = Category.objects.all()
    context = {
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,
        'all_posts': all_posts,
        'tag':tag
    }
    return render(request, 'Home/home.html', context)

class PostCommentDetailView(generic.TemplateView):
    template_name = "Home/post_detail.html"

    def get(self,request,pk):
        form = AddCommentsForm()
        post = get_object_or_404(Post, pk=pk)
        latest_posts = Post.objects.order_by('-creation_datetime')[:3]
        tag = Category.objects.all()
        if(request.user.is_anonymous):
            args = {
                'form': form,
                'latest_posts': latest_posts,
                'post': post,
                'tag': tag
            }
        else:
            fav = post.blogger_set.filter(user=request.user)
            args = {
                'form': form,
                'latest_posts': latest_posts,
                'post': post,
                'tag': tag,
                'fav': fav
            }

        return render(request, self.template_name, args)

    def post(self, request, pk):
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse('Personal:loginregister'))
        else:
            form = AddCommentsForm(request.POST)
            if form.is_valid():
                commentForm = form.save(commit=False)
                commentForm.blogger = request.user
                commentForm.post = Post.objects.filter(pk=pk).first()
                commentForm.save()
                comment = form.cleaned_data['comment']
                args={
                    'form': form,
                    'comment':comment
                }
            return HttpResponseRedirect(reverse('Home:post_detail', kwargs={'pk':pk}))

def tag_posts(request, tag_id):
    tag = Category.objects.get(id=tag_id)
    tag_posts = Post.objects.filter(category=tag)
    all_posts = Post.objects.all()
    context = {
        'tag': tag,
        'tag_posts': tag_posts,
        'all_posts': all_posts
    }
    return render(request, 'Home/tag_posts.html', context)


def search(request):
    all_posts = Post.objects.all()
    all_bloggers = User.objects.all()
    form = BlogSearchForm()
    post_results = []
    blogger_results = []
    search_term = None
    if request.method == 'POST':
        form = BlogSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            post_results = list(all_posts.filter(title__icontains=search_term))
            blogger_results = list(all_bloggers.filter(Q(first_name__icontains=search_term)|Q(last_name__icontains=search_term)))

    return render(request, 'Home/search_results.html', {'form': form, 'post_results': post_results, 'blogger_results': blogger_results, 'keyword': search_term})

def favView(request,pk):
    if(request.user.is_anonymous):
        return HttpResponseRedirect(reverse('Personal:loginregister'))
    else:
        post = get_object_or_404(Post, pk=pk)
        if (request.POST.get('fav')=='yes'):
            request.user.blogger.fav_post.add(post)
        else:
            request.user.blogger.fav_post.remove(post)
        return HttpResponseRedirect(reverse('Home:post_detail', kwargs={'pk':pk}))

# class Home(TemplateView):
#     template_name = 'home1.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['latest_blogs'] = Post.objects.all().order_by('-creation_datetime')[:5]
