# Documentation for this API: http://www.vam.ac.uk/api/

from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access
import random

class VictoriaAlbertMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        self.api_url = 'http://www.vam.ac.uk/api/json/museumobject/search'
        self.parameters = {
            'images': 1,
            'limit': 45,
        }

        # Attempts to solve https://github.com/shannonturner/art-games/issues/11:

        random_flag = random.choice((False, False, False, False, True)) # 20% chance
        if random_flag:
            self.parameters['random'] = 1

        date_flag = random.choice((False, True, None, None, None)) # 40% chance of using before or after
        if date_flag is None:
            pass # The 'before' / 'after' parameters will not be used this time.
        elif date_flag:
            after_dates = (-3000, -2000, -1000, 0, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900)
            after_date = random.choice(after_dates)
            self.parameters['after'] = after_date
        elif not date_flag:
            before_dates = (2100, 1900, 1800, 1700, 1600, 1500, 1400, 1300, 1200, 1100, 1000, 0)
            before_date = random.choice(before_dates)
            self.parameters['before'] = before_date

        # Make offset happen 50% of the time
        offset_flag = random.choice((True, False))
        if offset_flag:
            # Weight lower offsets more heavily
            random_maximum = []
            for x in range(30, 0, -1):
                random_maximum.extend(range(x))

            random_maximum = random.choice(random_maximum) * 1000

            self.parameters['offset'] = random.randint(0, random_maximum)

        # Keep a close eye on the letter flag block.
        # This might do more harm than good since it always returns the same group of artworks
        # Don't be afraid to comment this part out
        letter_flag = random.choice((False, False, False, False, False, False, False, False, False, True))
        # 10% chance, plus one of the other flags must also be set.
        if letter_flag and any((offset_flag, date_flag, random_flag)):
            self.parameters['q'] = random.choice('bcdefghijklmnopqrstuvwy')

    def get_artwork(self, **kwargs):

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