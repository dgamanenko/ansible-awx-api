
import hashlib
from tower import AnsibleTower
from secrets import AnsibleTowerGetSecrets

class AnsibleTowerGetData(AnsibleTower):
    def __init__(self, scope='read', tokens_file='secret_keys', run_from='remote'):
        secrets = AnsibleTowerGetSecrets(tokens_file=tokens_file, run_from=run_from, scope=scope).get_secrets()
        super(AnsibleTowerGetData, self).__init__(host=secrets['awx_host'], token=secrets['awx_token'], schema=secrets['awx_schema'])

    # Get tower organizations
    def organizations(self, org_id=None):
        results = self.tower_api_get('organizations', curr_id=org_id)
        return results

    # Get tower organization id by name
    def organization_id_by_name(self, inv_name):
        result={}
        if isinstance(inv_name,basestring):
            organizations = self.organizations()
            for org in organizations['results']:
                if org['name'] == inv_name:
                    result = org['id']
        return result

    # Get tower projects
    def projects(self, project_id=None):
        results = self.tower_api_get('projects', curr_id=project_id)
        return results

    # Get tower inventories
    def inventories(self, inv_id=None):
        results = self.tower_api_get('inventories', curr_id=inv_id)
        return results

    # Get tower credentials
    def credentials(self, cred_id=None):
        results = self.tower_api_get('credentials', curr_id=cred_id)
        return results

    # Get tower credential id by name
    def credentials_id_by_name(self, cred_name):
        result={}
        if isinstance(cred_name,basestring):
            credentials = self.credentials()
            for cred in credentials['results']:
                if cred['name'] == cred_name:
                    result = cred['id']
        return result

    # Get tower credential_types
    def credential_types(self, cred_type_id=None):
        results = self.tower_api_get('credential_types', curr_id=cred_type_id)
        return results

    # Get tower workflow_job_templates
    def workflow_job_templates(self, wjt_id=None):
        results = self.tower_api_get('workflow_job_templates', curr_id=wjt_id)
        return results

    # Get tower job_templates
    def job_templates(self, jt_id=None):
        results = self.tower_api_get('job_templates', curr_id=jt_id)
        return results

    # Get tower extra_vars from workflow_job_templates
    def workflow_job_templates_extra_vars(self, wjt_id=None, hexdigest=False):
        try:
            wjt_data = self.workflow_job_templates(wjt_id)
            results = {}
            for res in wjt_data['results']:
                if hexdigest:
                    results[res['id']] = {'hexdigest': self.__extra_vars_hexdigest(res['extra_vars'])}
                else:
                    results[res['id']] = {'extra_vars': res['extra_vars']}
            return results
        except:
            print('Unable to retrieve extra_vars from Tower Workflow Job Templates')

    # Get tower extra_vars from job_templates
    def job_templates_extra_vars(self, jt_id=None, hexdigest=False):
        try:
            wjt_data = self.job_templates(jt_id)
            results = {}
            for res in wjt_data['results']:
                if hexdigest:
                    results[res['id']] = {'hexdigest': self.__extra_vars_hexdigest(res['extra_vars'])}
                else:
                    results[res['id']] = {'extra_vars': res['extra_vars']}
            return results
        except:
            print('Unable to retrieve extra_vars from Tower Job Templates')

    # Get tower variables from inventories
    def inventories_variables(self, inv_id=None, hexdigest=False):
        try:
            inv_data = self.inventories(inv_id)
            results = {}
            if not inv_id:
                for res in inv_data['results']:
                    if hexdigest:
                        results[res['id']] = {'hexdigest': self.__extra_vars_hexdigest(res['variables'])}
                    else:
                        results[res['id']] = {'variables': res['variables']}
                return results
            else:
                if hexdigest:
                    results[inv_id] = {'hexdigest': self.__extra_vars_hexdigest(inv_data['variables'])}
                else:
                    results[inv_id] = {'variables': inv_data['variables']}
                return results
        except:
            print('Unable to retrieve variables from Tower Inventory')

    # Get hexdigest from extra_vars
    def __extra_vars_hexdigest(self, extra_vars=None):
        try:
            m = hashlib.md5()
            m.update(extra_vars)
            result = m.hexdigest()
            return result
        except:
            print('Unable to retrieve hexdigest for extra_vars')

