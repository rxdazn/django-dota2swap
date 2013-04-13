import requests
from dota2swap import settings_local


class   SteamWrapper():
    ''' Steam API wrapper '''

    API_KEY = settings_local.STEAM_API_KEY

    @classmethod
    def _send_request(cls, endpoint, *args, **kwargs):
        params = {'key': cls.API_KEY}
        params.update(kwargs)
        request = requests.get(endpoint, params=params)
        return request.json()

    @classmethod
    def get_schema(cls):
        return cls._send_request(settings_local.STEAM_SCHEMA_ENDPOINT, language='en')

    @classmethod
    def get_player_inventory(cls, player_id):
        return cls._send_request(settings_local.STEAM_PLAYER_ITEMS_ENDPOINT, SteamID=player_id)
