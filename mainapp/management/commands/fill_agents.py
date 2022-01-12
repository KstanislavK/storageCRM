import os
import json

from django.core.management.base import BaseCommand

from partnersapp.models import PartnersList

JSON_PATH = 'mainapp/management/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        agents = load_from_json('agents')

        PartnersList.objects.all().delete()
        for agent in agents:
            new_agent = PartnersList(**agent)
            new_agent.save()
