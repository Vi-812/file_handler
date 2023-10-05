from celery import shared_task
from .models import File


@shared_task
def process_file(file_id):
    try:
        file = File.objects.get(pk=file_id)
        # Здесь можно выполнить обработку файла
        # Например, что-то сделать с file.file.path
        file.processed = True
        file.save()
    except File.DoesNotExist:
        pass  # Обработка ошибки, если файл не найден
