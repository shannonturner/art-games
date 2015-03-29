from django.db import models
import datetime

class Artwork(models.Model):
    
    title = models.CharField(max_length=255, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True) # Most dates would be year-only or in an incorrect format for DateField
    art_type = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)

    image_url = models.CharField(max_length=255) 
    external_url = models.CharField(max_length=255, null=True, blank=True) # For the artwork's page on the website, if applicable
    external_id = models.CharField(max_length=255, null=True, blank=True)
    museum = models.CharField(max_length=255)

    from_api = models.CharField(max_length=255, null=True, blank=True)

    # dimensions = models.CharField(max_length=255, null=True, blank=True)
    # credit = models.CharField(max_length=255, null=True, blank=True)
    # accession = models.CharField(max_length=255, null=True, blank=True)
    # photo_credit = models.CharField(max_length=255, null=True, blank=True)

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return '{0}'.format(self.title)

class Vote(models.Model):

    " Each time two artworks are lined up side by side, both the winning and losing artwork will be saved. "
    
    won = models.ForeignKey(Artwork, related_name='won')
    lost = models.ForeignKey(Artwork, related_name='lost')

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

    def __unicode__(self):
        return 'Artwork {0} won over Artwork {1}'.format(won, lost)

