from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import News, Category
from .forms import NewsForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Вьюха через класс более современно
class HomeView(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    mixin_prop = 'hellow world'
    paginate_by = 2

    # queryset = News.objects.select_related('category')

    # extra_context = {'title': 'Главная'}  # Что бы добавить какие-то переменные в контекст №1

    # Что бы добавить какие-то переменные в контекст №2
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная')
        return context

    # Что бы не возвращать все с бд, а только то что определим сами
    # .select_related('category') использум что бы было меньше запросов к бд, типа будет мало но с join
    # .prefetch_related('') используют когда мени ту мени
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


# Вьюха через функцию более современно
def index(request):
    news = News.objects.all()
    # res = '<h1>Список новостей</h1>'
    # for item in news:
    #     res += f'<div><p>{item.title}</p><p>{item.content}</p></div><hr>'
    context = {
        'news': news,
        'title': 'Список новостей'
    }

    return render(request, 'news/index.html', context)


# class Feedback(LoginRequiredMixin, CreateView):
#     form_class = ContactForm
#     template_name = 'news/feedback.html'
#     success_url = reverse_lazy('home')
#     raise_exception = True

@login_required(login_url='home')
def feedback(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['text'], 'knazevoleh@gmail.com',
                             ['vladganggg@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('feedback')
            else:
                messages.error(request, 'Ошибка отправки!')
        else:
            messages.error(request, 'Ошибка!')
    else:
        form = ContactForm()
    return render(request, 'news/feedback.html', {'form': form})


class NewsCategory(MyMixin, ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'
    pk_url_kwarg = 'pk'


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)

    context = {
        'news': news,
        'category': category
    }

    return render(request, 'news/category.html', context)


# def index_second(request):
#     return HttpResponse('<h1>Hack the world!</h1>')

def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    context = {
        'news_item': news_item,
    }

    return render(request, 'news/view_news.html', context)


class AddNews(LoginRequiredMixin, CreateView):
    # login_url = 'home'
    raise_exception = True

    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse('home')
    success_url = reverse_lazy('home')


def add_news(request):
    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            # news = News.objects.create(**form.cleaned_data)   # Для форм не связвнных с моделями
            news = form.save()
            return redirect(news)
    else:
        form = NewsForm()

    context = {
        'form': form,
    }

    return render(request, 'news/add_news.html', context)
