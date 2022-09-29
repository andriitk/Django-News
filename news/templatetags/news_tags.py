from django.db.models import Count, F
from django import template
from news.models import Category
from django.core.cache import cache

register = template.Library()


# Simple user tag
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()


# Inclusion user tag
@register.inclusion_tag('news/list_categories.html')
def show_categories():
    # cache.get_or_set('categories',
    #                  Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)

    categories = cache.get('categories')
    if not categories:
        # categories = Category.objects.all()
        # return {'categories': categories, 'arg1': arg1, 'arg2': arg2}
        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
        cache.set('categories', categories, 30)
    return {'categories': categories}
