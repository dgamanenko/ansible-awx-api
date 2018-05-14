
from tower import AnsibleTower
from get import AnsibleTowerGetData
from secrets import AnsibleTowerGetSecrets

class AnsibleTowerCreateData(AnsibleTowerGetData):
    def __init__(self, scope='write', tokens_file='secret_keys', run_from='remote'):
        super(AnsibleTowerCreateData, self).__init__(scope=scope, tokens_file=tokens_file, run_from=run_from)

    # Tower inventories API POST
    def inventory_post(self, payload):
        
        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])

        result = self.tower_api_post('inventories', curr_id=None, payload=payload)
        return result

    # Tower inventory hosts API POST
    def inventory_host_post(self, inv_id, payload):

        url_path_rpart = 'inventories/{}/hosts'.format(inv_id)
        result = self.tower_api_post(url_path_rpart, curr_id=None, payload=payload)
        return result

    # Tower inventory source API POST
    def inventory_source_post(self, inv_id, payload):
        #Get credential id if credential in payload set as name
        if isinstance(payload['credential'],basestring):
            credential = self.credentials()
            for cred in credential['results']:
                if cred['name'] == payload['credential']:
                    payload['credential'] = (cred['id'])

        url_path_rpart = 'inventories/{}/inventory_sources'.format(inv_id)
        result = self.tower_api_post(url_path_rpart, curr_id=None, payload=payload)
        return result

    # Tower credentials API POST
    def credentials_post(self, payload):
        #Get credential_type id if credential_type in payload set as name
        if isinstance(payload['credential_type'],basestring):
            credential_type = self.credential_types()
            for cred_type in credential_type['results']:
                if cred_type['name'] == payload['credential_type']:
                    payload['credential_type'] = (cred_type['id'])

        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])

        result = self.tower_api_post('credentials', curr_id=None, payload=payload)
        return result

    # Tower job_template API POST
    def job_template_post(self, payload, labels_payload = []):
        result = self.tower_api_post('job_templates', curr_id=None, payload=payload)
        for l_pl in labels_payload:
            self.job_template_labels(jt_id=result['id'], payload=l_pl)
        return result

    # Tower workflow_job_template API POST
    def workflow_job_template_post(self, payload, labels_payload = []):
        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])
        result = self.tower_api_post('workflow_job_templates', curr_id=None, payload=payload)
        for l_pl in labels_payload:
            self.workflow_job_template_labels(wjt_id=result['id'], payload=l_pl)
        return result

    # Tower projects API POST
    def project_post(self, payload):
        
        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])

        result = self.tower_api_post('projects', curr_id=None, payload=payload)
        return result

    # Tower job_template labels API POST
    def job_template_labels(self, jt_id, payload):

        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])

        url_path_rpart = 'job_templates'
        response = self.tower_api_post(url_path_rpart=url_path_rpart+'/{}'.format(jt_id) +'/'+'labels', curr_id=None, payload=payload)
        return response

    # Tower job_template labels API POST
    def workflow_job_template_labels(self, wjt_id, payload):
        #Get organization id if organization in payload set as name
        if isinstance(payload['organization'],basestring):
            payload['organization'] = self.organization_id_by_name(payload['organization'])

        url_path_rpart = 'workflow_job_templates'
        response = self.tower_api_post(url_path_rpart=url_path_rpart+'/{}'.format(wjt_id) +'/'+'labels', curr_id=None, payload=payload)
        return response
