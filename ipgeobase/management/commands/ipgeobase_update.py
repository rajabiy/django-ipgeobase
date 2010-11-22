#coding: utf-8

from django.core.management.base import NoArgsCommand
from django.db import connection, transaction
from django_ipgeobase.conf import *
from zipfile import ZipFile
from urllib import urlopen
from cStringIO import StringIO
from django.core.mail import mail_admins
from django_ipgeobase.models import City, Country, District, Region, IPGeoBase
from django.utils.encoding import force_unicode
from pytils.translit import slugify

ERROR_SUBJECT = u"Ошибка команды ipgeobase_update"
send_message = IPGEOBASE_SEND_MESSAGE_FOR_ERRORS

try:
    country = Country.objects.get(alias = 'russia')
except:
    country = Country(name = u'Россия', alias = 'russia')
    country.save()

city_hashes = {}
district_hashes = {}
region_hashes = {}

def get_or_create_city(region, city_name):
    
    key = u'%s%s%s'%(region.country, region, city_name)    
    if city_hashes.has_key(key): return city_hashes[key]
    
    try:
        city = City.objects.get(region = region, name = city_name)
    except:
        city = City(region = region, name = city_name, alias = slugify(city_name).lower())
        city.save()
    
    city_hashes[key] = city
    return city

def get_or_create_district(country, name):
    key = u'%s%s'%(country, name)
    
    if district_hashes.has_key(key): return district_hashes[key]
    try:
        district = Dictrict.objects.get(country = country, name = name)
    except:
        district = District(country = country, alias = slugify(name).lower(), name = name)
        district.save()
        
    district_hashes[key] = district
    return district

def get_or_create_region(country, name):
    
    key = u'%s%s'%(country, name)
    if region_hashes.has_key(key): return region_hashes[key]
    try:
        region = Region.objects.get(country = country, name = name)
    except:
        alias = slugify(name).lower()
        region = Region(country = country, name = name, alias = alias)
        region.save()
    
    region_hashes[key] = region
    return region

class Command(NoArgsCommand):
    """С помощью этой команды база с ip-блоками обновляется с сайта-источника"""
    def handle(self, *args, **options):
        print u"Скачиваем zip-архив базы с сайта-источника..."
        f = urlopen(IPGEOBASE_SOURCE_URL)
        buffer = StringIO(f.read())
        f.close()
        print u"Распаковываем..."
        zip_file = ZipFile(buffer)
        try:
            file_read = zip_file.read(IPGEOBASE_FILENAME)
        except KeyError:
            message = u"Файл %s не найден в архиве" % IPGEOBASE_FILENAME
            if send_message:
                mail_admins(subject=ERROR_SUBJECT, message=message)
            return message
        zip_file.close()
        buffer.close()
        print u"Начинаем обновление..."
        lines = file_read.decode(IPGEOBASE_CODING).split('\n')
        transaction.enter_transaction_management()
        try:
            transaction.managed(True)
            print u"Удаляем старые записи в таблице ipgeobase..."
            IPGeoBase.objects.all().delete()
            print u"Записываем новое..."
            data =  [l.split('\t') for l in lines if l.strip()]
            for line in data:
                region = get_or_create_region(country, force_unicode(line[4]))
                city = get_or_create_city(region, force_unicode(line[3]))
                district = get_or_create_district(country, force_unicode(line[5]))
                
                base = IPGeoBase(
                    ip_block = line[0],
                    start = line[1],
                    end = line[2],
                    city = city,
                    region = region,
                    district = district,
                    latitude = line[6],
                    longitude = line[7]
                )
                
                base.save()
            
            transaction.commit()
        except Exception, e:
            message = u"Данные не обновлены:", e
            if send_message:
                mail_admins(subject=ERROR_SUBJECT, message=message)
            return message
        finally:
            transaction.rollback()
            transaction.leave_transaction_management()
        return u"Таблица ipgeobase обновлена."
