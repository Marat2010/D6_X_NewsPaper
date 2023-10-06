from django.urls import path
from .views import PostsList, PostDetailView, PostSearch, PostCreateView, \
    PostUpdateView, PostDeleteView, CategoriesListView, CategoryDetailView

app_name = 'news'
urlpatterns = [
    path('', PostsList.as_view(), name='posts'),
    path('search/', PostSearch.as_view()),

    path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),

    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),

]

