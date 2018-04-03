#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from django.core.wsgi import get_wsgi_application

def populate():
    product_1 = add_product(id="CZ01-009", name="音乐板电源线", order='200', date="2017-02-25")
    add_process(product=product_1, name='断线', code='E1#')
    add_process(product=product_1, name='压接', code='A20')
    add_process(product=product_1, name='端子装配', code='C1')
    add_process(product=product_1, name='裁及装套套', code='T3')
    add_process(product=product_1, name='成品检查', code='')

    product_2 = add_product(id="CZ01-001", name="6类网线", order='1000', date="2018-03-01")
    add_process(product=product_2, name="断线", code="E1#")
    add_process(product=product_2, name='压接', code='A20')
    add_process(product=product_2, name='端子装配', code='C1')
    add_process(product=product_2, name='成品检查', code='')

    for c in Products.objects.all():
        for p in Process.objects.filter(product=c):
            print "- {0} -{1}" .format(str(c), str(p))

def add_produce(product, process, material, assignednum, operator, producenum, processdes, detectlog, inspectlog, inspectdate, inspector, desc)
    j = Produce.objects.get_or_create(product=product, process=process, material=material, assigned_num=assignednum, operator=operator,
                                      produce_num=producenum, process_des=processdes, detect_log=detectlog, inspect_date=inspectdate,
                                      inspector=inspector, description=desc)
    return j

def add_process(product, name, code):
    k = Process.objects.get_or_create(product=product, process_name=name, process_code=code)[0]
    return k


def add_material(name, code, inventory, used):
    l = Material.objects.get_or_create(material_name=name, material_code=code, inventory_num=inventory, used_num=used)[0]
    return l

def add_product(id, name, order, date):
    m = Products.objects.get_or_create(product_id=id, product_name=name, order_num=order, deliver_date=date)[0]
    return m

# Start execution here!
if __name__ == '__main__':
    print "Starting database population script..."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testdj.settings")
    application = get_wsgi_application()
    from dailywork.models import Products, Process, Material, Produce
    populate()