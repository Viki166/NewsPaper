from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating_author = models.IntegerField('рейтинг пользователя', default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        sum = 0
        sum_rating_article = Post.objects.filter(author=self.id, article_or_news=1).values('author', 'post_rating')
        for i in sum_rating_article:
            sum = i['post_rating'] * 3
        sum_rating_comment = Comment.objects.filter(author=self.id).values('author', 'rating_comment')
        for j in sum_rating_comment:
            sum = sum + j['rating_comment']
        self.rating_author = sum


class Category(models.Model):
    name_of_category = models.CharField('название категории', max_length=100, unique=True)

    def __str__(self):
        return self.name_of_category


class Post(models.Model):
    ARTICLE = '1'
    NEWS = '2'

    CHOICE = (
        (ARTICLE, 'Article'),
        (NEWS, 'News'),
    )
    article_or_news = models.CharField('поле с выбором - статья или новость',
                                       max_length=1, choices=CHOICE,
                                       default=ARTICLE)
    date_of_creation_post = models.DateTimeField('дата и время создания', auto_now_add=True)
    header = models.CharField('заголовок статьи или новости', max_length=200)
    post_text = models.TextField('текст статьи или новости')
    post_rating = models.IntegerField('рейтинг статьи или новости', default=0)
    category = models.ManyToManyField(Category, through='PostCategory', null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.header

    def preview(self):
        text_len = 124
        if len(self.post_text) > text_len:
            text_str = self.post_text[:text_len] + '...'
        else:
            text_str = self.post_text
        return text_str

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField('текст комментария', max_length=500)
    date_of_creation_comment = models.DateTimeField('дата и время создания комментария', auto_now_add=True)
    rating_comment = models.IntegerField('рейтинг комментария', default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()