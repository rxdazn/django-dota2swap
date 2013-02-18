"""
Steam OpenID support.

"""
import urlparse, json, urllib
from django.utils import timezone

from social_auth.backends import OpenIDBackend, OpenIdAuth, USERNAME

# Steam configuration
STEAM_URL = 'http://steamcommunity.com/openid'
STEAM_API_URL = 'http://api.steampowered.com'
STEAM_API_KEY = '384CA80B9C501046885E0B9B0F40F79E'

class SteamBackend(OpenIDBackend):
    """Steam OpenID authentification backend"""
    name = 'steam'

    def get_user_details(self, response):
        values = super(SteamBackend, self).get_user_details(response)
        steamid = urlparse.urlsplit(response.identity_url).path.split('/')[3]
        
        values[USERNAME] = steamid
        
        try:
            c = urllib.urlopen(STEAM_API_URL + "/ISteamUser/GetPlayerSummaries/v0002/?key=" + STEAM_API_KEY +
                "&steamids=" + steamid + "&format=json")
            content = json.loads(c.read())
            values['first_name'] = content['response']['players'][0]['personaname']
            values['avatar'] = content['response']['players'][0]['avatarfull']
        except:
            values['first_name'] = steamid
        return values

    def get_user_id(self, details, response):
        return urlparse.urlsplit(response.identity_url).path.split('/')[3]


class SteamAuth(OpenIdAuth):
    """Steam OpenID authentication"""
    AUTH_BACKEND = SteamBackend

    def uses_redirect(self):
        """Steam uses redirect"""
        return True

    def openid_url(self):
        """Returns Steam authentication URL"""
        return STEAM_URL


# Backend definition
BACKENDS = {
    'steam': SteamAuth,
}


def update_user_details(backend, details, response, user, is_new=False, *args,
                        **kwargs):
    """Update user username and last_login"""
    for name, value in details.iteritems():
        if name == USERNAME:
            setattr(user, name, value)
    user.last_login = timezone.now()
    user.save()