from celery.utils.log import get_task_logger

from QuizApp.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, name='add')
def add(self, x, y):
    logger.info(f'Adds {x} + {y}')
    return x + y


@app.task(bind=True, name='send_mail')
def send_mail(self, username):
    mail = f'{username}@gmail.com'  # as example
    logger.info(mail)
    # Here celery task should send mail to registered user with some text
