from django.urls import path, include
# from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, LoginView, LogoutView, upgrade_to_author, subscribe_to, unsubscribe_from

app_name = 'sign'
urlpatterns = [
   # path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
   # path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
   path('login/', LoginView.as_view(), name='login'),
   path('logout/', LogoutView.as_view(), name='logout'),
   path('signup/', RegisterView.as_view(), name='signup'),
   path('getauthor/', upgrade_to_author, name='getauthor'),
   path('subscribe/<int:pk>', subscribe_to, name='subscribe'),
   path('unsubscribe/<int:pk>', unsubscribe_from, name='unsubscribe'),
]

