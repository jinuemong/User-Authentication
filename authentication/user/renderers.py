
import json
from rest_framework.renderers import JSONRenderer

# JSon 
# Manage errors in json format
class UserJsonRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self,data,media_type=None,renderer_context=None):

        # If an error is thrown from the view, the error is included in the internal data.

        errors = data.get('errors',None) # receive error

        # Tokens are in byte format, so serialization is not possible
        # Decode required before rendering: decryption process
        # Store only the token separately
        token = data.get('token',None)

        # find error -> return data (not user key save)
        if errors is not None:
            return super(UserJsonRenderer,self).render(data)
        
        # Handling when tokens are stored as bytes
        if token is not None and isinstance(token,bytes):
            data['token'] = token.decode('utf-8') # charset

        # date into user key -> return
        return json.dumps({
            'user':data
        })
