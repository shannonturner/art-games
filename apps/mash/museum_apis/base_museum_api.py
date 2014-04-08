class BaseMuseumApi(object):

    " Generic Base class for an Art Museum's API "

    def get_artwork(self, **kwargs):
        
        " Get one artwork and return details as a dictionary. Returns False if failed so a different artwork may be retrieved. "

    def save_artwork_details(self, **kwargs):

        " Save artwork details in the database for statistics and later use with other games. "

        from apps.mash.models import Artwork

        exists = Artwork.objects.filter(**kwargs)

        if exists:
            if len(exists) == 1:
                return exists
            else:
                print "\n[INFO] Artwork may have a duplicate in the system? \n", exists, "\n"
                return exists[0]
        else:
            artwork = Artwork(**kwargs)
            artwork.save()
            return artwork