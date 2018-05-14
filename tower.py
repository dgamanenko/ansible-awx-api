
import urllib2, json

class AnsibleTower(object):
    def __init__(self, host, token, schema='http', api_current_version='v2'):
        ''' Constructor for this class. '''
        self.host = host
        self.schema = schema
        self.token = token
        self.api_current_version = api_current_version
        self.headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + self.token
        }
        self.awx_api_url_base = self.schema + '://' + self.host + '/api/' + self.api_current_version +'/'

    # Tower API GET
    def tower_api_get(self, url_path_rpart, curr_id=None, payload={}):
        try:
            add_to_url = ''

            if curr_id != None:
                add_to_url = curr_id + '/'

            req = urllib2.Request(
                url = self.awx_api_url_base + url_path_rpart + '/' + add_to_url,
                headers = self.headers
            )
            response = urllib2.urlopen(req)
            results = json.loads(response.read())

            return results
        except urllib2.URLError as error:
            print('Unable to retrieve Tower {0} due to error : {1} '. format(url_path_rpart, error))

    # Tower API POST
    def tower_api_post(self, url_path_rpart, curr_id=None, payload={}):
        
        add_to_url = ''

        if curr_id != None:
            add_to_url = curr_id + '/'

        url = self.awx_api_url_base + url_path_rpart + '/' + add_to_url

        try:
            
            upd_req = urllib2.Request(
                url = url,
                data = json.dumps(payload),
                headers = self.headers
            )

            upd_req.get_method = lambda: 'POST'

            response = urllib2.urlopen(upd_req)
            try:
                result = json.loads(response.read())
            except:
                result = {}
            return result

        except urllib2.URLError as error:
            print('Unable to make API POST: {0} '. format(error))

    # Tower API PUT
    def tower_api_put(self, url_path_rpart, curr_id, payload):
        
        add_to_url = ''

        if curr_id != None:
            add_to_url = curr_id + '/'

        url = self.awx_api_url_base + url_path_rpart + '/' + add_to_url

        try:
            
            upd_req = urllib2.Request(
                url = url,
                data = json.dumps(payload),
                headers = self.headers
            )

            upd_req.get_method = lambda: 'PUT'

            response = urllib2.urlopen(upd_req)
            result = json.loads(response.read())

            return result

        except urllib2.URLError as error:
            print('Unable to make API PUT: {0} '. format(error))

    # Tower API PUT (Update existing)
    def tower_api_put_update(self, url_path_rpart, curr_id, payload):

        data = self.tower_api_get(url_path_rpart, curr_id = curr_id)
        url = self.awx_api_url_base + url_path_rpart + '/' + curr_id + '/'
        data.update(payload)

        print(data)

        try:
            
            upd_req = urllib2.Request(
                url = url,
                data = json.dumps(data),
                headers = self.headers
            )

            upd_req.get_method = lambda: 'PUT'

            response = urllib2.urlopen(upd_req)
            result = json.loads(response.read())

            return result

        except urllib2.URLError as error:
            print('Unable to make API PUT (Update): {0} '. format(error))

    # Tower API PATCH
    def tower_api_patch(self, url_path_rpart, curr_id, payload):

        url = self.awx_api_url_base + url_path_rpart + '/' + curr_id + '/'
        
        try:
            upd_req = urllib2.Request(
                url = url,
                data = json.dumps(payload),
                headers = self.headers
            )

            upd_req.get_method = lambda: 'PATCH'

            response = urllib2.urlopen(upd_req)
            result = json.loads(response.read())

            return result

        except urllib2.URLError as error:
            print('Unable to make API PATCH: {0} '. format(error))
