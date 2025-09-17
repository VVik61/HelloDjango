import datetime
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CkeditorCustomStorage(FileSystemStorage):
    def __save(self, name, content):
        folder_name = datetime.datetime.now().strftime('%Y%m%d%')
        name = os.path.join(folder_name, name)
        return super().save(name, content)

    location = os.path.join(settings.MEDIA_ROOT, 'uploads/')
    base_url = 'http://127.0.0.1:8000/'