import json
import os
from datetime import date

from ordersapp.models import TKList, OrderList, OrderProductsList
from partnersapp.models import PartnersList
from storageapp.models import CategoryList, BatchList, MakerList, NomenList, ProductList
from transportapp.models import RideList

today = date.today().strftime('%d%m%y')


def write_backup(name, object_list):
    with open(f'backups/{today}/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(object_list, f, ensure_ascii=False, indent=4, default=str)


def partner_list():
    objects = PartnersList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "partner_city": item.partner_city,
            "address": item.address,
            "contact_person": item.contact_person,
            "contact_phone": item.contact_phone,
            "contact_email": item.contact_email,
            "is_active": item.is_active,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = PartnersList._meta.db_table
    write_backup(name, object_list)


def tk_list():
    objects = TKList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "logo": item.logo,
        }
        object_list.append(agent)

    name = TKList._meta.db_table
    write_backup(name, object_list)


def category_list():
    objects = CategoryList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "description": item.description,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = CategoryList._meta.db_table

    write_backup(name, object_list)


def batch_list():
    objects = BatchList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "delivery_date": item.delivery_date,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = BatchList._meta.db_table

    write_backup(name, object_list)


def maker_list():
    objects = MakerList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "country": item.country,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = MakerList._meta.db_table

    write_backup(name, object_list)


def nomen_list():
    objects = NomenList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "part_number": item.part_number,
            "category": item.category,
            "maker": item.maker,
            "description": item.description,
            "meters": item.meters,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = NomenList._meta.db_table

    write_backup(name, object_list)


def product_list():
    objects = ProductList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "name": item.name,
            "batch": item.batch,
            "amount": item.amount,
            "place": item.place,
            "is_active": item.is_active,
            "is_retail": item.is_retail,
            "slug": item.slug,
        }
        object_list.append(agent)

    name = ProductList._meta.db_table

    write_backup(name, object_list)


def order_list():
    objects = OrderList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "created_at": item.created_at,
            "partner": item.partner,
            "self_pickup": item.self_pickup,
            "tk": item.tk,
            "payed": item.payed,
            "shipped": item.shipped,
            "shipped_date": item.shipped_date,
            "for_delivery": item.for_delivery,
            "comment": item.comment,
            "user_creator": item.user_creator,
        }
        object_list.append(agent)

    name = OrderList._meta.db_table

    write_backup(name, object_list)


def orderproduct_list():
    objects = OrderProductsList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "product": item.product,
            "order": item.order,
            "batch": item.batch,
            "is_retail": item.is_retail,
            "amount": item.amount,
        }
        object_list.append(agent)

    name = OrderProductsList._meta.db_table

    write_backup(name, object_list)


def ride_list():
    objects = RideList.objects.all()
    object_list = list()

    for item in objects:
        agent = {
            "title": item.title,
            "address": item.address,
            "order": item.order,
            "description": item.description,
            "created_at": item.created_at,
            "delivered": item.delivered,
            "delivered_at": item.delivered_at,
        }
        object_list.append(agent)

    name = RideList._meta.db_table

    write_backup(name, object_list)


def do_backup():

    if not os.path.exists(f'backups/{today}'):
        os.makedirs(f'backups/{today}')

    partner_list()
    tk_list()
    category_list()
    batch_list()
    maker_list()
    nomen_list()
    product_list()
    order_list()
    orderproduct_list()
    ride_list()
