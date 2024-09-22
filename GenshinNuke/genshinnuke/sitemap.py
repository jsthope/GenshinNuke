from django.contrib.sitemaps import Sitemap
from base.models import Room
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sites.models import Site

class RoomsSitemap(Sitemap):
    def get_urls(self, site=None, protocol='None', **kwargs):
        site = Site(domain='genshinnuke.com', name='genshinnuke.com')
        return super(RoomsSitemap, self).get_urls(site=site, protocol='https', **kwargs)

    def items(self):
        return Room.objects.all()

    def lastmod(self, obj):
        return obj.updated
    
class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"

    def get_urls(self, site=None, protocol='None', **kwargs):
        site = Site(domain='genshinnuke.com', name='genshinnuke.com')
        return super(StaticViewSitemap, self).get_urls(site=site, protocol='https', **kwargs)
    def items(self):
        return ["home", "login", "register" , "logout", "create-room", "privacy-policy"]

    def location(self, item):
        return reverse(item)

