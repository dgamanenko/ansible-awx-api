#!/usr/bin/python

import json

class AnsibleTowerGetSecrets(object):

    def __init__(self, tokens_file='secret_keys', run_from='local', scope='read'):
        ''' Constructor for this class. '''
        self.tokens_file = tokens_file
        secrets = {}
        with open(self.tokens_file, 'r') as f:
            secrets = json.loads(f.read())

        if (run_from == 'local'):
            run = 'awx_api_local'
        elif (run_from == 'remote'):
            run = 'awx_api_remote'

        if (scope == 'read'):
            run_scope = 'awx_api_read_only_token'
        elif (scope == 'write'):
            run_scope = 'awx_api_write_access_token'

        try:
            self.awx_token = secrets[run][run_scope]
            self.awx_host = secrets[run]['awx_api_host']
            self.awx_schema = secrets[run]['awx_api_schema']
        except:
            print('Error: could not get secrets')

    # Get secrets
    def get_secrets(self):
        results = {'awx_token': self.awx_token, 'awx_host': self.awx_host, 'awx_schema': self.awx_schema}
        return results

