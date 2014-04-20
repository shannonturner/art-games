from django.db import models
from apps.mash.models import Artwork
import datetime

# Create your models here.

class NewTitle(models.Model):

    " A user-given title for untitled artworks "

    title = models.TextField(max_length=60)
    
    art = models.ForeignKey(Artwork, related_name='newtitle')

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())