from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'

    def ready(self):  # подключаем сигналы
        import news.signals



