# Documentation for this API: http://api.thewalters.org/

from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access

class WaltersMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        import random
        from art_credentials import walters_key

        self.api_url = 'http://api.thewalters.org/v1/objects'
        self.parameters = {
            'apikey': walters_key,
            'page': random.randint(1, 608) # 608 pages of 25 artworks = 15200
        }

    def get_artwork(self, **kwargs):

        import random
        import requests

        try:
            response = requests.get(self.api_url, timeout=5, params=self.parameters).json()
        except:
            return False, 'waltersmuseum' # If an error occurs here, the API is most likely no longer accepting requests

        response = access(response, ['Items'])

        artwork = {}

        available_choices = range(len(response))
        image_url = None

        while not image_url:

            choice = random.choice(available_choices)

            for image_size in ('Raw', 'Large', 'Medium', 'Small'):
                image_url = access(response, [choice, 'PrimaryImage', image_size])

                if image_url:
                    artwork['image_url'] = image_url
                    break
            else:
                available_choices.remove(choice)
            
            if image_url:
                break
        else:
            return False, 'waltersmuseum' # If none of the choices had a valid image

        artwork['from_api'] = 'Walters Museum'
        
        artwork['external_id'] = access(response, [choice, 'ObjectID'])
        if not artwork['external_id']:
            return False, 'waltersmuseum'

        artwork['title'] = access(response, [choice, 'Title'])

        if not artwork['title'] or artwork['title'] == 'null':
            artwork['title'] = 'Untitled'

        artwork['external_url'] = access(response, [choice, 'ResourceURL'])
        artwork['source'] = 'Walters Museum'
        artwork['museum'] = 'Walters Museum'
        artwork['artist'] = access(response, [choice, 'Creator'])
        artwork['art_type'] = access(response, [choice, 'Medium'])
        
        artwork['description'] = access(response, [choice, 'Description'])
        if not artwork['description'] or artwork['description'] == 'null':
            artwork['description'] = None

        artwork['date'] = access(response, [choice, 'DateText'])

        try:
            artwork_model = self.save_artwork_details(**artwork)
        except:
            return False, 'waltersmuseum'

        return artwork_model, 'waltersmuseum'