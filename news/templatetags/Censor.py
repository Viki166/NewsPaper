from django import template

register = template.Library()  # если мы не зарегистрируем наши фильтры, то Django никогда не узнает, где именно их искать и фильтры потеряются

profanity_list = ['дурак', 'дебил', 'идиот']  # "плохие слова" для проверки


@register.filter(name='censor')  # регистрируем наш фильтр под именем censor, чтоб django понимал, что это именно фильтр, а не простая функция
def censor(value, arg):   # первый аргумент здесь это то значение, к которому надо применить фильтр, второй аргумент — это аргумент фильтра, т.е. примерно следующее будет в шаблоне value|censor:arg
    for word in profanity_list:
        if word.lower() in value.lower():
            return value.replace(word, arg)   # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон
        else:
            return value
