from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Author
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['article_news'] = Post.CHOICE
        return context

    def post(self, request, *args, **kwargs):
        author_id = request.POST['author']
        article_or_news = request.POST['article_or_news']
        header = request.POST['header']
        post_text = request.POST['post_text']
        category_id = request.POST['category']
        post = Post(author_id=author_id, article_or_news=article_or_news, header= header, post_text = post_text, category_id=category_id)
        post.save()
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



