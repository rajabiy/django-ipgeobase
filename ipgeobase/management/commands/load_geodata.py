#coding: utf-8

from django.core.management.base import BaseCommand
from django.conf import settings
from urllib import urlopen
import gzip
import zipfile
from ipgeobase.models import Country

GEO_COUNTRIES = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz'
GEO_COUNTRIES_CSV = 'http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip'
#GEO_CITIES = 'http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz'

class Command(BaseCommand):
    help = 'Command from load data for geotargeting'

    def handle(self, *args, **options):
        print u"Loading database archive.."
        f = urlopen(GEO_COUNTRIES)
        gzip_countries = f.read()
        f.close()
        fcountries = open(settings.GEOIP_PATH+'GeoIP.dat.gz', 'wb')
        fcountries.write(gzip_countries)
        fcountries.close()    
        
        print u"Unpacking..."
        countries = gzip.open(settings.GEOIP_PATH+'GeoIP.dat.gz')
        out = open(settings.GEOIP_PATH+'GeoIP.dat', 'wb')
        out.write(countries.read())
        out.close()
        countries.close()
        print u"OK"
        
        print u"Loading countries list.."
        f = urlopen(GEO_COUNTRIES_CSV)
        zip_countries = f.read()
        f.close()
        fcountries = open(settings.GEOIP_PATH+'countries.csv.zip', 'wb')
        fcountries.write(zip_countries)
        fcountries.close()    
        
        print u"Unpacking..."
        countries =  zipfile.ZipFile(settings.GEOIP_PATH+'countries.csv.zip')
        out = open(settings.GEOIP_PATH+'countries.csv', 'wb')
        out.write(countries.read('GeoIPCountryWhois.csv'))
        out.close()
        countries.close()
        print u"OK"
        
        hashes = {}
        def get_or_add_country(code, name):
            code = code.upper()
            if hashes.has_key(code): return hashes[code]
            try:
                country = Country.objects.get(alias = code)
            except:
                print code, name
                country = Country(alias = code, name = name)
                country.save()
                
            hashes[code] = country                
            return country
        
        print u"Write countries to database"
        
        import csv
        rows = csv.reader(open(settings.GEOIP_PATH+'countries.csv', 'rb'))
        for row in rows:            
            get_or_add_country(row[4], row[5])
        print "OK"