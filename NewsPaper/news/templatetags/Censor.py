from django import template

register = template.Library()
profanity_list = ['новые', 'после', 'деталей']  # "плохие слова" для проверки


@register.filter(name='censor')
def censor(value, arg):
    for word in profanity_list:
        if word.lower() in value.lower():
            return value.replace(word, arg)
