from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm, UserRegisterForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-id']
    form_class = PostForm
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class Posts(View):

    def get(self, request):
        posts = Post.objects.order_by('-id')
        p = Paginator(posts, 1)
        posts = p.get_page(request.GET.get('page', 1))
        data = {
            'posts': posts,
        }
        return render(request, 'search.html', data)


class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


class PostCreateView(CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    login_url = '/accounts/login/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
    #     return context


# @login_required
# def upgrade_me(request):
#     user = request.user
#     authors_group = Group.objects.get(name='authors')
#     if not request.user.groups.filter(name='authors').exists():
#         authors_group.user_set.add(user)
#     return redirect('/news')


# class MyView(PermissionRequiredMixin, View):
#     permission_required = ('<app>.<action>_<model>',
#                            '<app>.<action>_<model>')
#
#
# class AddNews(PermissionRequiredMixin, CreateView):
#     permission_required = ('news.post.add_post', 'news.post.change_post')
#
#
class PostDeleteView(DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/search/'


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/news')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/news')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('/news')