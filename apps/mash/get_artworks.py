import random

import time

def get_artworks(**kwargs):

    " From available APIs, choose two random images. "

    specific_apis = kwargs.get('specific_apis')

    if not specific_apis:
        from available_apis import available_apis
    else:
        available_apis = specific_apis

    both_apis = []

    both_apis.append(random.choice(available_apis.keys()))
    both_apis.append(random.choice(available_apis.keys()))

    for index, one_api in enumerate(both_apis):
        while (both_apis[index] == one_api or not both_apis[index]) and len(available_apis) > 1:
            both_apis[index] = available_apis[one_api]().get_artwork()

    # This will only happen in the rare instances that all available APIs are down. 
    if both_apis[0] in available_apis and both_apis[1] in available_apis:
        both_apis[0] = both_apis[1] = {
            'source': 'Service Currently Unavailable :(',
            'title': 'The external museum services powering this site is not accepting our requests at this time.',
        }

    # In the rare case of two images being identical, one_api still contains the right side's api to re-pull from
    while both_apis[0] == both_apis[1] and not both_apis[1]:
        both_apis[1] = available_apis[one_api]().get_artwork()

    return both_apis