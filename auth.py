import pickle
import yahoo.application
from const import CONSUMER_KEY, CONSUMER_SECRET, APPLICATION_ID, TOKEN_STORAGE


oauthapp = \
    yahoo.application.OAuthApplication(CONSUMER_KEY, CONSUMER_SECRET,
                                       APPLICATION_ID)

# check if we've got a stored token
try:
    pkl_file=open(TOKEN_STORAGE, 'rb')
    access_token=pickle.load(pkl_file)
    pkl_file.close()
except:
    access_token=None

if access_token:
    print 'You have an access token: %s' % str(access_token.to_string().strip())
else:
    # get request token
    print '* Obtain a request token ...'
    request_token = oauthapp.get_request_token()

    # authorize the request token
    print '\n* Authorize the request token ...'
    print '\nAuthorization URL:\n%s' % oauthapp.get_authorization_url(request_token)
    verifier = raw_input('Please authorize the url above ^^^')

    # now the token we get back is an access token
    print '\n* Obtain an access token ...'
    access_token = oauthapp.get_access_token(request_token, verifier.strip())
    print '\nkey: %s' % str(access_token.key)
    print 'secret: %s' % str(access_token.secret)
    print 'yahoo guid: %s' % str(access_token.yahoo_guid)

    pkl_file=open(TOKEN_STORAGE, 'wb')
    pickle.dump(access_token, pkl_file)
    pkl_file.close()


# set access token for oauth app
oauthapp.token = access_token
oauthapp.refresh_access_token(access_token)
