from django.shortcuts import render, get_object_or_404
# redirect to login page
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from .models import Post
from django.core.paginator import Paginator

# Create new function
# Handle trafic in home page of blog
# def home(request):
#    return HttpResponse('<h1>Blog Home</h1>')


# def about(request):
#    return HttpResponse('<h1>Blog About</h1>')

# add dummy data
# posts2 = [
#     {
#         'author': 'Author A',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'Aug 23,2019'
#     },
#     {
#         'author': 'Author B',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'Aug 25,2019'
#     }
# ]


# Loading template
def home(request):
    context = {  # create dectionary
        # 'posts': posts2  # create key #get in dummy data
        'posts': Post.objects.all()  # get in database
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  # change order list/ new -> old
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
# create individual post view


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # take the instance set the author as current user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        # take the instance set the author as current user
        form.instance.author = self.request.user
        return super().form_valid(form)
# check user is author

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
# check user is author

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def menu(request):
    return render(request, 'blog/menu.html')


def where(request):
    return render(request, 'blog/where.html')
