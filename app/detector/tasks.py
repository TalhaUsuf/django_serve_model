from celery import shared_task
from detector.models import widgets # because app has been listed under installed apps as 'detector'

# The @shared_task decorator lets you create tasks without having any concrete app instance:
# tasks are shared across all the apps i.e. all apps can call this function
# @shared_task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')




@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_widgets():
    return widgets.objects.count()


@shared_task
def rename_widget(widget_id, name):
    w = widgets.objects.get(id=widget_id)
    w.name = name
    w.save()
