# coding: utf-8

from django.db import models
import socket
import struct

class IPGeoBaseManager(models.Manager):
    def by_ip(self, ip):
        """Отдает объекты для найденных соответствий по ip.
        Причем, наиболее точное совпадение в начале списка"""
        number = struct.unpack('!L', socket.inet_aton(ip))[0]
        return super(IPGeoBaseManager, self).get_query_set().filter(start__lte=number, end__gte=number).order_by('end', '-start')
