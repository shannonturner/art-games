# Whenever adding a new museum API, be sure to add it here.
from apps.mash.museum_apis.luce_museum_api import LuceMuseumApi

available_apis = {
    'luce': LuceMuseumApi
}