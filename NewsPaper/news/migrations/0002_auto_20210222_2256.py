# Generated by Django 3.1.6 on 2021-02-22 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, through='news.PostCategory', to='news.Category'),
        ),
    ]
