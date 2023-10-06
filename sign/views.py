from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from .forms import RegisterForm, LoginForm
from news.models import Category


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'sign/register.html'
    success_url = '/news/'

    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get_or_create(name='common')[0]
        user.groups.add(group)  # добавляем нового пользователя в эту группу
        user.save()
        return super().form_valid(form)


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'sign/login.html'
    success_url = '/news/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'sign/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required
def upgrade_to_author(request):
    user = request.user
    print("=== 0 user.groups ==:", user.groups.all())
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')


@login_required()
def subscribe_to(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    # print('===11===', category)

    if not category.subscribers.filter(pk=user.id).exists():
        category.subscribers.add(user)
        # print('===22===', category.subscribers.all())

    # return redirect('/news/categories')
    return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def unsubscribe_from(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    print('===11===', category)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    # return redirect('/news/categories')
    return redirect(request.META.get('HTTP_REFERER'))

