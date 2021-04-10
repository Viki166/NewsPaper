# runapscheduler.py
import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from ...models import Category, Post
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


def my_job():
    users = User.objects.all().order_by('id')
    for user in users:
        user_category = Category.objects.filter(subscribers=user)
        for last_user_category in user_category:
            news = Post.objects.filter(category=last_user_category).order_by('-id')[0]
            news_id = news.id
            news_id = str(news_id)
            link = 'http://127.0.0.1:8000/news/search/'+news_id
            str(link)
            msg = EmailMultiAlternatives(
                subject=f'{news.header}',
                body=f'Здравствуй {user.username}, Новая статья в твоем любимом разделе! {news.post_text[:50]}... Ссылка на новость: {link}',
                from_email='bobby.loner27@gmail.com',
                to=[user.email],
            )

            msg.send()


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="mon"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")