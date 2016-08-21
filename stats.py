import oauthlib.oauth
import simplejson
import pandas as pd
from auth import oauthapp
from const import SPORTS_API_URL


def get_stats(start_idx=0):
    url = SPORTS_API_URL + \
        "/leagues;league_keys=314.l.199215/players;start=%d/stats" % start_idx
    guid = oauthapp.token.yahoo_guid
    parameters = { 'format': 'json' }
    request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(
                oauthapp.consumer, token=oauthapp.token, http_method='GET',
                http_url=url, parameters=parameters)
    request.sign_request(oauthapp.signature_method_hmac_sha1,
                         oauthapp.consumer, oauthapp.token)
    response = simplejson.loads(oauthapp.client.access_resource(request))
    return response


#  ========
#  = MAIN =
#  ========
player_data = []

for start_idx in range(0, 2775, 25):
    print start_idx
    r = get_stats(start_idx)
    players = r['fantasy_content']['leagues']['0']['league'][1]['players']

    for k in players.iterkeys():
        if k == 'count':
            continue
        else:
            p = players[k]['player']
            player_key = p[0][0]['player_key']
            full_name = p[0][2]['name']['full']
            position = p[0][-3]['eligible_positions'][0]['position']
            points = p[1]['player_points']['total']
            player_data.append({'player_key': player_key, 'full_name': full_name,
                                'position': position, 'points': points})

print len(player_data)
# for p in player_data:
#     print p
df = pd.DataFrame(player_data).set_index('player_key')
df.to_csv('stats2013.csv')

# response['fantasy_content']['leagues']['0']['league'][1]['players']['0']['player'][0][0]['player_key']
# response['fantasy_content']['leagues']['0']['league'][1]['players']['0']['player'][0][2]['name']['full']
# response['fantasy_content']['leagues']['0']['league'][1]['players']['0']['player'][0][-4]['position_type']
# response['fantasy_content']['leagues']['0']['league'][1]['players']['0']['player'][1]['player_points']['total']
