# coding: utf-8

from django.contrib import admin
from django_ipgeobase.models import City, Country, District, Region, IPGeoBase

class RegionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"alias": ("name",),}
    list_display=('name', 'alias')
    
admin.site.register(Region, RegionAdmin)

class DistrictAdmin(admin.ModelAdmin):
    prepopulated_fields = {"alias": ("name",),}
    list_display=('name', 'alias')
    
admin.site.register(District, DistrictAdmin)
    
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"alias": ("name",),}
    list_display=('name', 'alias')
    
admin.site.register(Country,CountryAdmin)

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"alias": ("name",),}
    list_display=('name', 'alias')

admin.site.register(City,CityAdmin)

class IPGeoBaseAdmin(admin.ModelAdmin):
    list_display=('ip_block', 'region', 'city')

admin.site.register(IPGeoBase, IPGeoBaseAdmin)
