from apps.mash.museum_apis.base_museum_api import BaseMuseumApi
from nested_access import access

class LuceMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        from apps.mash.museum_apis.art_credentials import luce_application_id

        self.random_boundaries = (1, 31114)
        self.api_url = 'http://edan-api.si.edu/metadataService'
        self.parameters = {
            'applicationID': luce_application_id,
            'rows': '1',
            'start': '0',
            'wt': 'json',
            'fq': 'online_media_type:Images'
        }

    def get_artwork(self, **kwargs):

        import random
        import requests
        from requests.auth import HTTPBasicAuth

        from apps.mash.museum_apis.art_credentials import luce_username, luce_password

        artwork_id = random.randint(self.random_boundaries[0], self.random_boundaries[1])
        self.parameters['start'] = artwork_id

        try:
            response = requests.get(self.api_url, timeout=0.1, params=self.parameters, auth=HTTPBasicAuth(luce_username, luce_password)).json()
        except:
            return False, 'luce' # If an error occurs here, the API is most likely no longer accepting requests

        artwork = {}

        artwork['from_api'] = 'luce'
        artwork['external_id'] = artwork_id

        artwork['image_url'] = access(response, ['response','docs',0,'descriptiveNonRepeating','online_media','media',0,'content'])
        artwork['title'] = access(response, ['response', 'docs', 0, 'descriptiveNonRepeating', 'title', 'content'])
        artwork['external_url'] = access(response, ['response', 'docs', 0, 'descriptiveNonRepeating', 'record_link'])
        artwork['source'] = access(response, ['response', 'docs', 0, 'freetext', 'dataSource', 0, 'content'])
        artwork['artist'] = access(response, ['response', 'docs', 0, 'freetext', 'name', 0, 'content'])
        artwork['art_type'] = access(response, ['response', 'docs', 0, 'freetext', 'objectType', 0, 'content'])
        artwork['description'] = access(response, ['response', 'docs', 0, 'freetext', 'physicalDescription', 0, 'content'])
        artwork['date'] = access(response, ['response', 'docs', 0, 'freetext', 'date', 0, 'content'])

        try:
            artwork_model = self.save_artwork_details(**artwork)
        except:
            return False, 'luce'

        # Sample model instance
        # {'created_at': datetime.datetime(2014, 3, 31, 2, 18, 46, 161577, tzinfo=<UTC>), 'art_type': u'Graphic Arts-Print', 'description': u'lithograph on paper', 'artist': u'Louis Silverstein, born New York City 1919-1994', 'museum': u'', 'title': u'Crucible, from the American Absract Artists 50th Anniversary Print Portfolio', '_state': <django.db.models.base.ModelState object at 0x1041cde90>, 'from_api': u'luce', 'updated_at': datetime.datetime(2014, 3, 31, 2, 18, 46, 161608, tzinfo=<UTC>), 'source': u'Smithsonian American Art Museum', 'image_url': u'http://americanart.si.edu/images/1987/1987.52.39_1a.jpg', 'date': u'1987', 'external_id': u'15515', 'id': 1, 'external_url': u'http://americanart.si.edu/collections/search/artwork/?id=22412'}

        return artwork_model, 'luce'