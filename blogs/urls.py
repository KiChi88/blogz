from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blogs'
urlpatterns = [
    path('login', auth_views.login, name='login'),
    path('logout', auth_views.logout, name='logout'),

    path('', views.HomePage.as_view(), name='index'),

    path('subscriptions', views.Subscriptions.as_view(), name='subscriptions'),
    path('subscriptions/all', views.SubscriptionsAll.as_view(), name='subscriptions_all'),
    path('subscribe/<int:id>', views.Subscribe.as_view(), name='subscribe'),
    path('search', views.Search.as_view(), name='search'),

    path('create_post', views.CreatePost.as_view(), name='create_post'),
    path('new_posts', views.NewPosts.as_view(), name='new_posts'),
    path('post/<int:pk>', views.Post.as_view(), name='post'),
    path('post/read/<int:id>', views.PostRead.as_view(), name='post_read'),

]