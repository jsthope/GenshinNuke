from django.contrib.sitemaps import Sitemap
from base.models import Room
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.contrib import sitemaps
from django.urls import reverse


class RoomsSitemap(Sitemap):
    def items(self):
        return Room.objects.all()

    def lastmod(self, obj):
        return obj.updated
    
class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        return ["home", "login", "register" , "logout", "create-room", "privacy-policy"]

    def location(self, item):
        return reverse(item)

