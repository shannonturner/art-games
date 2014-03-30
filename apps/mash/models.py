from django.db import models

class Artwork(models.Model):
    
    title = models.CharField(max_length=255, null=True, blank=True)
    artist = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=255, null=True, blank=True) # Most dates would be year-only or in an incorrect format for DateField
    type_ = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)

    image_url = models.CharField(max_length=255) 
    external_url = models.CharField(max_length=255, null=True, blank=True) # For the artwork's page on the website, if applicable
    external_id = models.CharField(max_length=255, null=True, blank=True)
    museum = models.CharField(max_length=255)

    from_api = models.CharField(max_length=255, null=True, blank=True)

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

class Vote(models.Model):

    " Each time two artworks are lined up side by side, both the winning and losing artwork will be saved. "
    
    won = models.ForeignKey(Artwork)
    lost = models.ForeignKey(Artwork)

    # Auto-generated timestamps
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=True, default=datetime.datetime.now())

