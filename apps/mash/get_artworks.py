import random
import time

def get_artworks(**kwargs):

    " From available APIs, choose two random images. "

    specific_apis = kwargs.get('specific_apis')

    if not specific_apis:
        from available_apis import available_apis
    else:
        available_apis = specific_apis

    # Get total number of artworks available
    total_artworks = 0

    for key in available_apis.keys():
        total_artworks += available_apis[key][1]

    total_artworks_text = 'Currently sourcing {0:,} artworks from {1} museum APIs.'.format(total_artworks, len(available_apis))

    both_apis = []

    both_apis.append(random.choice(available_apis.keys()))
    both_apis.append(random.choice(available_apis.keys()))

    for index, one_api in enumerate(both_apis):

        if len(available_apis) == 1:
            time.sleep(1)

        if len(available_apis) > 1:
            both_apis[index], which_api = available_apis[one_api][0]().get_artwork()
        else:
            both_apis[index] = False

    # This will only happen in the rare instances that all available APIs are down. 
    if not both_apis[0] and not both_apis[1]:
        both_apis[0] = both_apis[1] = {
            'source': 'Service Currently Unavailable :(',
            'title': 'The external museum services powering this site is not accepting our requests at this time.<br>This may be a temporary outage; <b>please load the page again!</b>',
        }

    # In the rare case of two images being identical, one_api still contains the right side's api to re-pull from
    while both_apis[0] == both_apis[1] and both_apis[1]:
        both_apis[1] = available_apis[one_api][0]().get_artwork()

    both_apis.append({'total_artworks': total_artworks_text})

    return both_apis