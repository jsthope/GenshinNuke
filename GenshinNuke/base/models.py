from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.core.exceptions import ValidationError
from urllib.parse import urlparse,parse_qs
from django.urls import reverse

# checks
def check_damage(value):
    if int(value) < 0: raise ValidationError("Damage can't be lower than 0")
    if int(value) >= 10_000_000: raise ValidationError("Damage can't be higher than 10M")
        
def check_constellation(value):
    if int(value) > 6:
        if int(value) < 0: raise ValidationError("Constellations can't be lower than 0")
        raise ValidationError("Constellations can't be higher than 6")
    
def check_refinement(value):
    if int(value) < 1: raise ValidationError("Refinement can't be lower than 1")
    if int(value) > 5: raise ValidationError("Refinement can't be higher than 5")

#https://stackoverflow.com/questions/4356538/how-can-i-extract-video-id-from-youtubes-link-in-python
def get_video_id(value):
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    raise ValidationError("The url is wrong")

# tags
class Weapon(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    data = models.JSONField()

    class Meta():
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    weapon_type = models.CharField(max_length=200)
    data = models.JSONField()

    class Meta():
        ordering = ['name']

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(null=True,max_length=35)

    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    weapon = models.ForeignKey(Weapon, on_delete=models.SET_NULL, null=True)

    constellation = models.IntegerField(null=True, validators=[check_constellation])
    refinement = models.IntegerField(null=True, validators=[check_refinement])


    damage = models.IntegerField(null=True, validators=[check_damage])
    proofURL = models.URLField(null=True, validators=[get_video_id])
    view = models.ManyToManyField(User, related_name='viewers',blank=True)
    description = models.TextField(null=True, blank=True,max_length=10000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta():
        ordering = ['-damage']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("room", args=[str(self.id)])
    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True, upload_to='pp/')

    def __str__(self):
        return self.user.username