# Whenever adding a new museum API, be sure to add it here.
# from apps.mash.museum_apis.luce_museum_api import LuceMuseumApi
# from apps.mash.museum_apis.rijks_museum_api import RijksMuseumApi
from apps.mash.museum_apis.victoria_albert_museum_api import VictoriaAlbertMuseumApi

available_apis = {
    # 'luce': (LuceMuseumApi, 31114) # as of 2013 November
    # 'rijksmuseum': RijksMuseumApi,
    'victoriaalbertmuseum': (VictoriaAlbertMuseumApi, 402101) # as of 2014 Apr 7
}