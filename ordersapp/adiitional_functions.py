from storageapp.models import NomenList


def count_sold_products(prods):

    objects = {}
    for obj in prods:

        if obj.product.name not in objects:
            objects[obj.product.name] = int(obj.amount)
        else:
            objects[obj.product.name] = objects[obj.product.name] + int(obj.amount)
    sorted_object = dict(sorted(objects.items(), key=lambda x: x[0]))  # Сортированный словарь по алфавиту

    # добавляю количество товара на складе
    for key, value in sorted_object.items():
        prod_sum = NomenList.objects.get(name=key).get_quantity()
        sorted_object[key] = [value, int(prod_sum)]

    return sorted_object
