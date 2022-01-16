import os
import json

from django.core.management.base import BaseCommand

from storageapp.models import Category

JSON_PATH = 'mainapp/management/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cats = load_from_json('prod_category')

        Category.objects.all().delete()
        for cat in cats:
            new_cat = Category(**cat)
            new_cat.save()
