import os
import json

from django.core.management.base import BaseCommand

from ordersapp.models import TKList

JSON_PATH = 'mainapp/management/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        tks = load_from_json('t_companies')

        TKList.objects.all().delete()
        for tk in tks:
            new_tk = TKList(**tk)
            new_tk.save()
