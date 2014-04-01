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

    debug_counter = 0

    for index, one_api in enumerate(both_apis):
        while both_apis[index] == one_api or not both_apis[index]:
            both_apis[index] = available_apis[one_api]().get_artwork()

    # In the rare case of two images being identical, one_api still contains the right side's api to re-pull from
    while both_apis[0] == both_apis[1] and not both_apis[1]:
        both_apis[1] = available_apis[one_api]().get_artwork()

    return both_apis