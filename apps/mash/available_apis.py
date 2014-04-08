# Whenever adding a new museum API, be sure to add it here.
# from apps.mash.museum_apis.luce_museum_api import LuceMuseumApi
# from apps.mash.museum_apis.rijks_museum_api import RijksMuseumApi
from apps.mash.museum_apis.victoria_albert_museum_api import VictoriaAlbertMuseumApi

available_apis = {
    # 'luce': LuceMuseumApi,
    # 'rijksmuseum': RijksMuseumApi,
    'victoriaalbertmuseum': VictoriaAlbertMuseumApi,
}