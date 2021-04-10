from django import template
from django.contrib.auth.models import Group

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются


@register.filter(name='has_group')
def has_group(user, common):
    group = Group.objects.get(name=common)
    return True if group in user.groups.all() else False
