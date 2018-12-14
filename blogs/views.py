from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User
from django.db.models import Q
from . models import Posts, Status
from . forms  import PostsForm

# Для просмотра страниц приложения необходима авторицазия
# Общий для всех представлений класс
class LoginRequiredBase(LoginRequiredMixin):
    login_url = '/login'
    redirect_field_name = '/'
    paginate_by = 10

# Главная страница
class HomePage(LoginRequiredBase, ListView):
    template_name = 'index.html'

    def get_queryset(self, *args, **kwargs):
        return Posts.objects.filter(user_id=self.request.user).order_by('-date')

# Создание нового поста
class CreatePost(LoginRequiredBase, CreateView):
    model = Posts
    form_class = PostsForm
    template_name = 'create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# Список читаемых блогов
class Subscriptions(LoginRequiredBase, ListView):
    template_name = 'subscriptions.html'

    def get_queryset(self, *args, **kwargs):
        return self.request.user.user.blogs.all()

# Список всех доступных блогов
class SubscriptionsAll(LoginRequiredBase, ListView):
    template_name = 'subscriptions_all.html'

    def get_queryset(self, *args, **kwargs):
        return User.objects.exclude(username=self.request.user.username).order_by('username')

# Подписаться / Отписаться
class Subscribe(LoginRequiredBase, View):
    # Получаем id пользователя: если на него подписаны, удаляем,
    # иначе добавляем в читаемые блоги
    def get(self, request, *args, **kwargs):
        person = User.objects.get(id=self.kwargs['id'])
        if person not in request.user.user.blogs.all():
            request.user.user.blogs.add(person)
            # Создаём необходимые статусы
            for post in person.posts_set.all():
                Status.objects.create(
                        user = request.user,
                        post = post
                    )
        else:
            request.user.user.blogs.remove(person)
            # Удаляем ненужные статусы при отписке
            for stat in Status.objects.filter(user=request.user):
                if stat.post in person.posts_set.all():
                    stat.delete()
        # Возвращаем пользователя к месту откуда был сделан запрос
        return HttpResponseRedirect(request.environ['HTTP_REFERER'] + '#' + str(self.kwargs['id']))

# Поиск всех доступных блогов
class Search(LoginRequiredBase, ListView):
    template_name = 'search.html'

    def get_queryset(self, *args, **kwargs):
        search = self.request.GET.get('search')
        if search:
            return User.objects.filter(
                    Q(username__icontains=search) | 
                    Q(first_name__icontains=search) |
                    Q(last_name__icontains=search)
                    ).exclude(username=self.request.user.username).order_by('username').distinct()
        return User.objects.none()

# Лента
class NewPosts(LoginRequiredBase, ListView):
    template_name = 'new_posts.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем статусы постов
        stats = [stat.post_id for stat in self.request.user.status_set.filter(read=True)]
        context['status'] = stats
        return context

    def get_queryset(self, *args, **kwargs):
        # Все посты на которые подписаны
        posts = [blog.posts_set.all() for blog in self.request.user.user.blogs.all()]
        if posts:
            query = posts[0]
            for post in posts[1:]:
                query |= post
        else:
            query = Posts.objects.none()
        return query.order_by('-date')

# Страница поста
class Post(LoginRequiredBase, DetailView):
    model = Posts
    template_name = 'post.html'

# Сообщение о прочтении поста
class PostRead(LoginRequiredBase, View):

    def get(self, request, *args, **kwargs):     
        status = request.user.status_set.get(post_id=self.kwargs['id'])
        status.read = True
        status.save()
        # Возвращаем пользователя к месту откуда был сделан запрос
        return HttpResponseRedirect(request.environ['HTTP_REFERER'] + '#' + str(self.kwargs['id']))