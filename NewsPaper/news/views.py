from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404



class PostsList(ListView):  # Список всех объектов из базы данных
    model = Post  # Модель, объекты которой мы выводим
    template_name = 'posts.html'  # имя шаблона, в котором содержатся инструкции о том, как должны вывестись наши объекты
    context_object_name = 'posts'  # имя списка, в котором будут лежать все объекты
    queryset = Post.objects.order_by('-id')


class PostDetail(DetailView):  # представление,в котором будет отдельная новость
    model = Post  # модель
    template_name = 'post.html'  # шаблон
    context_object_name = 'post'  # название объекта


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-id']
    form_class = PostForm
    paginate_by = 10  # поставим постраничный вывод в 10 элементов

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        # берём значения для новой новости из POST-запроса отправленного на сервер
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новую новость
            form.save()
        return super().get(request, *args, **kwargs)  # отправляем пользователя обратно на GET-запрос

# В отличиe от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов (например, get- или post-, вспоминаем реквесты из 19-го модуля)
class Posts(View):

    def get(self, request):
        posts = Post.objects.order_by('-id')
        p = Paginator(posts, 1)  # создаём объект класса пагинатор, передаём ему список наших новостей и их количество для одной страницы
        posts = p.get_page(request.GET.get('page', 1))  # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектах в списке товаров хранится только нужная нам страница с товарами
        data = {
            'posts': posts,
        }
        return render(request, 'search.html', data)


# Дженерик для получения деталей о новости
class PostDetailView(DetailView):
    template_name = 'news/post_detail.html'
    queryset = Post.objects.all()


# дженерик для создания новости. Надо указать только имя шаблона и класс формы. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = 'news.add_author'


# дженерик для редактирования новости
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):  # аутентификация, проверка доступа
    template_name = 'news/post_create.html'
    form_class = PostForm
    login_url = '/accounts/login/'
    permission_required = 'news.change_author'

    def get_object(self, **kwargs): # метод get_object мы используем вместо queryset, чтобы получить информацию новости, которую мы собираемся редактировать
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления новости
class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'news/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/search/'
    permission_required = 'news.delete_author'

# идентификация пользователя
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


# регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            common_group = Group.objects.get(name='common')
            common_group.user_set.add(user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/news')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {"form": form})


@login_required  # декоратор проверки аутентификации
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


def user_logout(request):
    logout(request)
    return redirect('/news')


class Mailing(UpdateView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        category = get_object_or_404(Category, id=request.POST.get('category_id'))
        category.subscribers.add(user)
        return redirect('/news/search/')