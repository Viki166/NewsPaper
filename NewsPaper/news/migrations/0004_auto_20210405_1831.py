# Generated by Django 3.1.6 on 2021-04-05 15:31

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20210228_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('client_name', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rating_comment',
            field=models.IntegerField(default=None, verbose_name='рейтинг комментария'),
        ),
    ]
