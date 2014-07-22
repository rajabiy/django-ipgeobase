#coding: utf-8
from xml.etree import ElementTree
from urllib import urlopen

from django.core.management.base import BaseCommand
from django.utils.encoding import force_unicode
from ipgeobase.models import Country

COUNTRIES = 'http://unicode.org/repos/cldr/trunk/common/main/ru.xml'


class Command(BaseCommand):
    help = 'Команда на перевод названий стран в базе на названия из базы CLDR http://cldr.unicode.org'

    def handle(self, *args, **options):
        print u'Получаем названия стран'
        f = urlopen(COUNTRIES)
        xml = ElementTree.parse(f)

        def get_add_update_country(code, name):
            code = code.upper()
            try:
                country = Country.objects.get(alias=code)
                country.name = name
                country.save()
            except Country.DoesNotExist:
                print u'%s в Базе отсутствует' % (code, )

        print u'Обновление названий стран'

        for element in xml.iter('territory'):
            get_add_update_country(element.attrib.get('type'), force_unicode(element.text))
        print u'Все ok'