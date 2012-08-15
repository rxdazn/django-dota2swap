import json
import urllib
import settings_local

class   apiTester():
    ''' Steam API tester '''
    def __init__(self):
        self.api_key = settings_local.STEAM_API_KEY
        self.player_id = 'STEAM_0:0:34549338'
        #self.player_id = '34549338'

    def __sendRequest__(self, endpoint, *args, **kwargs):
        params = urllib.urlencode(dict([('key', self.api_key)] + kwargs.items()))
        print 'request params', params
        print 'requrl', (endpoint + '?%s') % params
        if not endpoint:
            print 'no endpoint'
            return
        http_resp = urllib.urlopen((endpoint + '?%s') % params)
        json_resp = json.loads(http_resp.read())
        return json_resp

    def getSchema(self):
        return self.__sendRequest__(settings_local.STEAM_SCHEMA_ENDPOINT)

    def getPlayerItems(self, player_id):
        return self.__sendRequest__(settings_local.STEAM_PLAYER_ITEMS_ENDPOINT, SteamID = player_id)

    def testRqst(self):
        return self.__sendRequest__(None, toto=3, tata=10, hihihihh='hello')

def test():
    x = apiTester()
    return x.getPlayerItems('76561198029364404')
