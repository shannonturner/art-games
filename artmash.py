
def artmash(self, **kwargs):

    import random
    import requests
    from requests.auth import HTTPBasicAuth

    # From available APIs, choose a random image

    available_apis = ['luce']

    both_apis = []

    both_apis.append(random.choice(available_apis))
    both_apis.append(random.choice(available_apis))

    for index, one_api in enumerate(both_apis):

        if one_api == 'luce':
            import mash_luce
            both_apis[index] = mash_luce.mash()

    while both_apis[0] == both_apis[1]: # In the rare case of two images being identical, one_api still contains the right side's api to re-pull from

        if one_api == 'luce':
            both_apis[1] = mash_luce.mash()
        
    # If a vote was cast, save it
    
    try:
        won = int(kwargs.get('w'))
    except Exception:
        won = None

    try:
        lost = int(kwargs.get('l'))
    except Exception:
        lost = None

    if won < 1:
        won = None

    if lost < 1:
        lost = None

    if won is not None and lost is not None:
        vote(won, lost)      
    
    ## ABOVE: COLLECT AND PROCESS
    ## BELOW: DISPLAY

    page_source = []

    page_source.append('<title>Favorite art choice game</title>')

    page_source.append('<link rel="stylesheet" type="text/css" href="./static/main.css"> <link rel="stylesheet" type="text/css" href="./static/gumby.css">')

    page_source.append('<div class="row"> <h2>Click the artwork you like better.</h2>')

    page_source.append('<div class="six columns quickMargin">')
    page_source.append(u'<a href="artmash?w={0}&l={1}"><img src="{2}" alt="{3}" title="{3}"></a>'.format(both_apis[0]['internal_id'], both_apis[1]['internal_id'], both_apis[0]['image_url'], both_apis[0]['title']).encode('ascii', 'ignore'))
    page_source.append('</div>')

    page_source.append('<div class="five columns">')
    page_source.append(u'<a href="artmash?w={0}&l={1}"><img src="{2}" alt="{3}" title="{3}"></a>'.format(both_apis[1]['internal_id'], both_apis[0]['internal_id'], both_apis[1]['image_url'], both_apis[1]['title']).encode('ascii', 'ignore'))
    page_source.append('</div>')

    page_source.append('</div>')

    page_source.append('<div class="row"> <div class="centered six columns" style="text-align: center;">')
    page_source.append('<h6><a href="artmash">Skip to see new art</a></h6><h4><a href="artmash_score">View the all-time favorites</a></h4> <a href="learn_more?id1={0}&id2={1}" target="_blank"><h4>Learn more about this art</h4></a>'.format(both_apis[0]['internal_id'], both_apis[1]['internal_id']))
    page_source.append('</div> </div>')

    return page_source


def vote(won, lost):

    import psycopg2
    from database_credentials import database_connection_details as database_connection_details

    database_connection = psycopg2.connect(database_connection_details)
    database_cursor = database_connection.cursor()

    try: # Just to be safe
        won = int(won)
        lost = int(lost)
    except Exception:
        return False

    insert_query = u"insert into artvote (won, lost) values ({0}, {1})".format(won, lost)

    database_cursor.execute(insert_query)
    database_connection.commit()

    return True
