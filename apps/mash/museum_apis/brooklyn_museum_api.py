# Brooklyn API Documentation: http://www.brooklynmuseum.org/opencollection/api/docs/

from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access

# Needed for removing HTML tags
# See also http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class BrooklynMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        import random
        from apps.mash.museum_apis.art_credentials import brooklyn_key

        start_index = random.randint(0, 29040)
        self.api_url = 'http://www.brooklynmuseum.org/opencollection/api'
        self.parameters = {
            'method': 'collection.search',
            'api_key': brooklyn_key,
            'version': 1,
            'format': 'json',
            'item_type': 'object',
            'date_range_begin': 10,
            'date_range_end': 3000,
            'max_image_size': 1536,
            'image_results_limit': 10,
            'start_index': start_index,
        }

    def get_artwork(self, **kwargs):

        import random
        import requests
        
        try:
            response = requests.get(self.api_url, timeout=15, params=self.parameters).json()
        except:
            return False, 'brooklyn' # If an error occurs here, the API is most likely no longer accepting requests

        artwork = {}

        artwork['from_api'] = 'brooklyn'
        available_choices = range(len(access(response, ['response', 'resultset', 'items'])))

        if len(available_choices) < 1:
            return False, 'brooklyn'

        image_url = None

        while not image_url:
            choice = random.choice(available_choices)

            # Determine the largest available image
            image_choices = access(response, ['response', 'resultset', 'items', choice, 'images'])
            max_available_size = -1
            if image_choices:
                for image_key, image_values in image_choices.items():
                    
                    # Skip non-image key/value pairs like results_limit and total
                    try:
                        int(image_key)
                    except:
                        continue 

                    uri = access(image_values, ['uri'])
                    
                    if not uri:
                        continue

                    available_size = uri.index('/size')
                    if available_size > 0:
                        available_size = int(uri[available_size + 5])

                    if available_size > max_available_size:
                        max_available_size = available_size
                        image_url = uri

                if image_url and max_available_size > 2: # more consistently give larger images
                    artwork['image_url'] = image_url
                    break
                else:
                    available_choices.remove(choice)
        else:
            # Last resort, if only small images are available in the resultset
            if image_url and max_available_size <= 2:

                # Try to get size 4 even if it's not given
                try:
                    r = requests.get(image_url.replace('/size{0}'.format(max_available_size), '/size4'))
                    if r.status_code == 200:
                        artwork['image_url'] = image_url.replace('/size{0}'.format(max_available_size), '/size4')
                    else:
                        artwork['image_url'] = image_url
                except:
                    artwork['image_url'] = image_url
            else:
                return False, 'brooklyn'

        artwork['external_id'] = access(response, ['response', 'resultset', 'items', choice, 'id'])

        if not artwork['external_id']:
            return False, 'brooklyn'

        artwork['title'] = access(response, ['response', 'resultset', 'items', choice, 'title'])
        artwork['external_url'] = access(response, ['response', 'resultset', 'items', choice, 'uri'])
        artwork['source'] = 'Brooklyn Museum'
        
        artwork['art_type'] = access(response, ['response', 'resultset', 'items', choice, 'medium'])
        
        artwork['description'] = access(response, ['response', 'resultset', 'items', choice, 'description'])
        if not artwork['description']:
            artwork['description'] = access(response, ['response', 'resultset', 'items', choice, 'label'])

        artwork['date'] = access(response, ['response', 'resultset', 'items', choice, 'object_date'])

        # Brooklyn API has multiple artists
        all_artists = access(response, ['response', 'resultset', 'items', choice, 'artists'])
        artwork['artist'] = []
        if all_artists:
            for artist in all_artists:
                artwork['artist'].append(artist['name'])

            artwork['artist'] = ', '.join(artwork['artist'])
        else:
            artwork['artist'] = ''

        # Brooklyn API descriptions sometimes have \r\n and HTML characters in them.  Let's remove them

        if artwork['description']:
            artwork['description'] = strip_tags(artwork['description'])
            artwork['description'] = artwork['description'].replace('\\r\\n', '')
        else:
            artwork['description'] = ''

        # Brooklyn API returns lots of escaped characters using backslashes.  Let's remove those.
        for key, value in artwork.items():
            if value:
                artwork[key] = value.replace('\\', '')

        try:
            artwork_model = self.save_artwork_details(**artwork)
        except:
            return False, 'brooklyn'

        # Sample model instance
        # {'created_at': datetime.datetime(2014, 3, 31, 2, 18, 46, 161577, tzinfo=<UTC>), 'art_type': u'Graphic Arts-Print', 'description': u'lithograph on paper', 'artist': u'Louis Silverstein, born New York City 1919-1994', 'museum': u'', 'title': u'Crucible, from the American Absract Artists 50th Anniversary Print Portfolio', '_state': <django.db.models.base.ModelState object at 0x1041cde90>, 'from_api': u'luce', 'updated_at': datetime.datetime(2014, 3, 31, 2, 18, 46, 161608, tzinfo=<UTC>), 'source': u'Smithsonian American Art Museum', 'image_url': u'http://americanart.si.edu/images/1987/1987.52.39_1a.jpg', 'date': u'1987', 'external_id': u'15515', 'id': 1, 'external_url': u'http://americanart.si.edu/collections/search/artwork/?id=22412'}

        return artwork_model, 'brooklyn'