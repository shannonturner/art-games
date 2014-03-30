class LuceMuseumApi(BaseMuseumApi):

    def __init__(self, **kwargs):

        super(LuceMuseumApi, self).__init__(self, **kwargs)

        from apps.mash.museum_apis.art_credentials import luce_application_id, luce_username, luce_password

        random_boundaries = (1, 31114)
        api_url = 'http://edan-api.si.edu/metadataService'
        parameters = {
            'applicationID': luce_application_id,
            'rows': '1',
            'start': '0',
            'wt': 'json',
            'fq': 'online_media_type:Images'
        }

    def get(self, **kwargs):

        import random
        import requests
        from requests.auth import HTTPBasicAuth

        artwork_id = random.randint(random_boundaries[0], random_boundaries[1])
        self.parameters['start'] = artwork_id

        try:
            response = requests.get(api_url, params=parameters, auth=HTTPBasicAuth(self.luce_username, self.luce_password)).json()
        except:
            return False # If an error occurs here, the API is most likely no longer accepting requests
            # In which case I may want to alert me

        try:
            artwork = {
                'from_api': 'luce'
                'external_id': artwork_id,
                'image_url': response['response']['docs'][0]['descriptiveNonRepeating']['online_media']['media'][0]['content'],
                'title': response['response']['docs'][0]['descriptiveNonRepeating']['title']['content'],
                'external_url': response['response']['docs'][0]['descriptiveNonRepeating']['record_link'],
                'source': response['response']['docs'][0]['freetext']['dataSource'][0]['content'],
                'artist': response['response']['docs'][0]['freetext']['name'][0]['content'],
                'type_': response['response']['docs'][0]['freetext']['objectType'][0]['content'],
                'description': response['response']['docs'][0]['freetext']['physicalDescription'][0]['content'],
                'date': response['response']['docs'][0]['freetext']['date'][0]['content'],
            }
        except:
            return False

        artwork_model = self.save_artwork_details(**artwork)

        return artwork_model
