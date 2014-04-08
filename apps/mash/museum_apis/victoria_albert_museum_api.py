# Documentation for this API: http://www.vam.ac.uk/api/

from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access

class VictoriaAlbertMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        import random

        self.api_url = 'http://www.vam.ac.uk/api/json/museumobject/search'
        self.parameters = {
            'random': 1,
            'images': 1,
            'limit': 1,
            'offset': random.randint(0, 1000000) # Better random than given by the API itself
        }

    def get_artwork(self, **kwargs):

        import random
        import requests

        try:
            response = requests.get(self.api_url, timeout=1, params=self.parameters).json()
        except:
            return False, 'victoriaalbertmuseum' # If an error occurs here, the API is most likely no longer accepting requests

        response = access(response, ['records'])
        choice = random.randint(0, len(response))

        artwork = {}

        artwork['from_api'] = 'Victoria and Albert Museum'
        artwork['external_id'] = access(response, [choice, 'pk'])

        image_url = access(response, [choice, 'fields', 'primary_image_id'])
        if image_url:
            artwork['image_url'] = "http://media.vam.ac.uk/media/thira/collection_images/{0}/{1}.jpg".format(image_url[:6], image_url)
        else:
            return False, 'victoriaalbertmuseum'

        artwork['title'] = access(response, [choice, 'fields', 'title'])

        if not artwork['title']:
            artwork['title'] = 'Untitled'

        # artwork['external_url'] = access(response, [])
        artwork['source'] = 'Victoria and Albert Museum'
        artwork['artist'] = access(response, [choice, 'fields', 'artist'])
        artwork['art_type'] = access(response, [choice, 'fields', 'object'])
        # artwork['description'] = access(response, [])
        artwork['date'] = access(response, [choice, 'fields', 'date_text'])

        # print artwork

        try:
            artwork_model = self.save_artwork_details(**artwork)
        except:
            return False, 'victoriaalbertmuseum'

        return artwork_model, 'victoriaalbertmuseum'