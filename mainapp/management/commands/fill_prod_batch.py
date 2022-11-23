import os
import json

from django.core.management.base import BaseCommand

from storageapp.models import BatchList

JSON_PATH = 'mainapp/management/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        batches = load_from_json('prod_batch')

        BatchList.objects.all().delete()
        for batch in batches:
            new_batch = BatchList(**batch)
            new_batch.save()
