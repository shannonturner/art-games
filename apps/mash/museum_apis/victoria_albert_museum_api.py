# Documentation for this API: http://www.vam.ac.uk/api/

from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access

class VictoriaAlbertMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        import random

        # Weight lower offsets more heavily
        random_maximum = []
        for x in range(30, 0, -1):
            random_maximum.extend(range(x))

        random_maximum = random.choice(random_maximum) * 1000

        self.api_url = 'http://www.vam.ac.uk/api/json/museumobject/search'
        self.parameters = {
            # 'random': 1,
            'images': 1,
            'limit': 45,
            'offset': random.randint(0, random_maximum) # Better random than given by the API itself
        }

    def get_artwork(self, **kwargs):

        import random
        import requests

        try:
            response = requests.get(self.api_url, timeout=1, params=self.parameters).json()
        except:
            return False, 'victoriaalbertmuseum' # If an error occurs here, the API is most likely no longer accepting requests

        response = access(response, ['records'])

        artwork = {}

        available_choices = range(len(response))
        image_url = None

        while not image_url:
            choice = random.choice(available_choices)
            image_url = access(response, [choice, 'fields', 'primary_image_id'])
            if image_url:
                artwork['image_url'] = "http://media.vam.ac.uk/media/thira/collection_images/{0}/{1}.jpg".format(image_url[:6], image_url)
                break
            else:
                available_choices.remove(choice)
        else:
            return False, 'victoriaalbertmuseum' # If none of the choices had a valid image

        artwork['from_api'] = 'Victoria and Albert Museum'
        artwork['external_id'] = access(response, [choice, 'pk'])
        if not artwork['external_id']:
            return False, 'victoriaalbertmuseum'

        artwork['title'] = access(response, [choice, 'fields', 'title'])

        if not artwork['title']:
            artwork['title'] = 'Untitled'

        # artwork['external_url'] = access(response, [])
        artwork['source'] = 'Victoria and Albert Museum'
        artwork['museum'] = 'Victoria and Albert Museum'
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