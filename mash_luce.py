
def mash():

    ' Retrieve a random image from the Luce API '

    import psycopg2
    import random
    import requests
    
    from database_credentials import database_connection_details
    from luce_credentials import username, password
    from requests.auth import HTTPBasicAuth

    database_connection = psycopg2.connect(database_connection_details)
    database_cursor = database_connection.cursor()

    THIS_API = 0 # My unique ID for the API, used with the external artwork ID for determining uniqueness among artworks

    max_random = 31114 # The Luce API has this many images

    external_id = random.randint(1, max_random)

    request_url = 'http://edan-api.si.edu/metadataService?applicationID={0}&rows=1&start={1}&wt=json&fq=online_media_type:Images'.format(username, external_id)

    response = requests.get(request_url, auth=HTTPBasicAuth(username, password)).json()

    artwork = {}

    artwork['this_api'] = THIS_API
    artwork['external_id'] = external_id
    artwork['image_url'] = response['response']['docs'][0]['descriptiveNonRepeating']['online_media']['media'][0]['content']
    artwork['title'] = response['response']['docs'][0]['descriptiveNonRepeating']['title']['content']
    artwork['url'] = response['response']['docs'][0]['descriptiveNonRepeating']['record_link']
    artwork['external_id2'] = artwork['url'][artwork['url'].index('=')+1:]

    select_query = "select id from artwork where this_api = {0} and external_id = '{1}'".format(artwork['this_api'], artwork['external_id'])

    database_cursor.execute(select_query)

    try:
        artwork['internal_id'] = database_cursor.fetchone()
    except TypeError:
        insert_query = """INSERT INTO artwork
        (this_api, title, url, image_url, external_id, external_id2)
        {0}, '{1}', '{2}', '{3}', '{4}', '{5}' RETURNING (id)
        """.format(artwork['this_api'], artwork['title'], artwork['url'], artwork['image_url'], artwork['external_id'], artwork['external_id2'])

        database_cursor.execute(insert_query)
        artwork['internal_id'] = database_cursor.fetchone()
        database_connection.commit()

    return artwork
        
