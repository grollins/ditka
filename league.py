import oauthlib.oauth
import simplejson
from auth import oauthapp
from const import SPORTS_API_URL


guid = oauthapp.token.yahoo_guid
url = SPORTS_API_URL + "/users;use_login=1/games/leagues"
print url
parameters = { 'format': 'json' }
request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(
            oauthapp.consumer, token=oauthapp.token, http_method='GET',
            http_url=url, parameters=parameters)
request.sign_request(oauthapp.signature_method_hmac_sha1,
                     oauthapp.consumer, oauthapp.token)
response = simplejson.loads(oauthapp.client.access_resource(request))

leagues = response['fantasy_content']['users']['0']['user'][1]['games']
for k in leagues.iterkeys():
    if k == 'count':
        continue
    else:
        L = leagues[k]
        try:
            if L['game'][0]['code'] == 'nfl':
                season = L['game'][0]['season']
                league_key = L['game'][1]['leagues']['0']['league'][0]['league_key']
                print k, season, league_key
            else:
                print k, "not an nfl league"
        except:
            print k, "not a valid fantasy league"

"""
OUTPUT
------
11 2011 257.l.85258
10 2010 242.l.154205
13 2013 314.l.199215
12 2012 273.l.188361
15 2015 348.l.213994
14 2014 331.l.515253
16 not a valid fantasy league
1 2004 101.l.299445
0 not an nfl league
3 not an nfl league
2 2003 79.l.181489
5 not an nfl league
4 not a valid fantasy league
7 2007 175.l.100668
6 2006 153.l.110730
9 2009 222.l.418940
8 2008 199.l.139102
"""