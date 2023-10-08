from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, FormView
from .forms import RegisterForm, LoginForm
from news.models import Category, Author
from django.conf import settings

DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL


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
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(authorUser=user)
    return redirect('/news')


@login_required()
def subscribe_to(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    # print('===11===', category)

    if not category.subscribers.filter(pk=user.id).exists():
        category.subscribers.add(user)
        email = user.email
        html = render_to_string(
            'mail/subscribe.html',
            {
                'category': category,
                'user': user
            },
        )
        msg = EmailMultiAlternatives(
            subject=f'Вы подписались на категорию {category}',
            body='',
            from_email=DEFAULT_FROM_EMAIL,
            to=[email, ],
        )

        msg.attach_alternative(html, 'text/html')

        try:
            msg.send()
        except Exception as e:
            print(e)
        # return redirect(request.META.get('HTTP_REFERER'))
        return redirect('news:categories')

    return redirect('news:categories')
    # return redirect('/news/categories')
    # return redirect(request.META.get('HTTP_REFERER'))


@login_required()
def unsubscribe_from(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    print('===11===', category)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('news:categories')
    # return redirect(request.META.get('HTTP_REFERER'))

