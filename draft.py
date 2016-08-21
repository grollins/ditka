import oauthlib.oauth
import simplejson
import pandas as pd
from auth import oauthapp
from const import SPORTS_API_URL


# url = SPORTS_API_URL + "/league/331.l.515253/draftresults" # 2014
url = SPORTS_API_URL + "/league/348.l.213994/draftresults" # 2015
guid = oauthapp.token.yahoo_guid
parameters = { 'format': 'json' }
request = oauthlib.oauth.OAuthRequest.from_consumer_and_token(
            oauthapp.consumer, token=oauthapp.token, http_method='GET',
            http_url=url, parameters=parameters)
request.sign_request(oauthapp.signature_method_hmac_sha1,
                     oauthapp.consumer, oauthapp.token)
response = simplejson.loads(oauthapp.client.access_resource(request))

draft_results = response['fantasy_content']['league'][1]['draft_results']

draft_data = []
for k in draft_results.iterkeys():
    if k == 'count':
        continue
    pick = draft_results[k]['draft_result']
    draft_data.append(pick)

df = pd.DataFrame(draft_data).set_index('player_key')
df.to_csv('draft.csv')
