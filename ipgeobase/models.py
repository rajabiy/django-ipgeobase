#coding: utf-8

from django.db import models
from ipgeobase.managers import IPGeoBaseManager
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    name = models.CharField(max_length=255,verbose_name=_('name'))
    alias = models.SlugField(verbose_name=_('alias'))
    priority = models.IntegerField(_('priority'), default = 0)
    
    class Meta:
        verbose_name=_('country')
        verbose_name_plural=_('countries')
        ordering = ('-priority', 'name', )

    def __unicode__(self):
        return self.name
        
class District(models.Model):
    country = models.ForeignKey(Country, verbose_name = _("country"))
    
    name = models.CharField(max_length=255,verbose_name=_('name'))
    alias = models.SlugField(verbose_name=_('alias'))
    
    class Meta:
        verbose_name=_('district')
        verbose_name_plural=_('districts')
        ordering = ('name', )

    def __unicode__(self):
        return u"%s, %s округ" %(self.country, self.name)
        
class Region(models.Model):
    country = models.ForeignKey(Country, verbose_name = _("country"))
    
    name = models.CharField(max_length=255,verbose_name=_('name'))
    alias = models.SlugField(verbose_name=_('alias'))
    
    class Meta:
        verbose_name=_('region')
        verbose_name_plural=_('regions')
        ordering = ('name', )

    def __unicode__(self):
        return u'%s, %s' % (self.country, self.name)
    
class City(models.Model):
    country = models.ForeignKey(Country, verbose_name = _("country"))
    region = models.ForeignKey(Region, verbose_name = _("region"), blank = True, null = True)
    
    name = models.CharField(_('name'), max_length=255)
    alias = models.SlugField(verbose_name=_('alias'))
    priority = models.IntegerField(_('priority'), default = 0)
    
    class Meta:
        verbose_name= _('city')
        verbose_name_plural= _('cities')
        ordering = ('-priority', 'name', )        
        
    def __unicode__(self):
        return self.name

class IPGeoBase(models.Model):
    """Таблица перечень блоков ip-адресов с координатами"""
    
    """Данное поле состоит из начального и конечного адресов блока, отделенных друг от друга пробелом, тире и пробелом"""
    ip_block = models.CharField(_('IP Addresses Block'), max_length=64)
    
    """IP-адрес иммет вид a.b.c.d, где a-d числа в диапазоне 0-255. Преобразование в число происходит по формуле 256³*a+256²*b+256*c+d"""
    start = models.BigIntegerField(_('initial IP-address of a block, converted to the number'), db_index=True)
    end = models.BigIntegerField(_('end IP-address of a block, converted to the number'), db_index=True)
    city = models.ForeignKey(City, verbose_name = _('city'))
    region = models.ForeignKey(Region, verbose_name = _('region'))
    district = models.ForeignKey(District, verbose_name = _('district'))
    
    latitude = models.FloatField(_('latitude'))
    longitude = models.FloatField(_('longitude'))

    objects = IPGeoBaseManager()
    
    def __unicode__(self):
        return self.ip_block
    
    class Meta:
        verbose_name= _('IP Block')
        verbose_name_plural= _('IP Base')
