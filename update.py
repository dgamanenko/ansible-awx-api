
from tower import AnsibleTower
from secrets import AnsibleTowerGetSecrets

class AnsibleTowerUpdateData(AnsibleTower):
    def __init__(self, scope='write', tokens_file='secret_keys', run_from='remote'):
        secrets = AnsibleTowerGetSecrets(tokens_file=tokens_file, run_from=run_from, scope=scope).get_secrets()
        super(AnsibleTowerUpdateData, self).__init__(host=secrets['awx_host'], token=secrets['awx_token'], schema=secrets['awx_schema'])

    # Tower job_template API PATCH
    def job_template_patch_update(self, jt_id, payload):
        result = self.tower_api_patch('job_templates', curr_id=jt_id, payload=payload)
        return result

    # Tower job_template API PUT
    def job_template_put_update(self, jt_id, payload):
        result = self.tower_api_put_update('job_templates', curr_id=jt_id, payload=payload)
        return result

    # Tower workflow_job_template API PATCH
    def workflow_job_template_patch_update(self, wjt_id, payload):
        result = self.tower_api_patch('workflow_job_templates', curr_id=wjt_id, payload=payload)
        return result

    # Tower workflow_job_template API PUT
    def workflow_job_template_put_update(self, wjt_id, payload):
        result = self.tower_api_put_update('workflow_job_templates', curr_id=wjt_id, payload=payload)
        return result

    # Tower inventory API PATCH
    def inventory_patch_update(self, inv_id, payload):
        result = self.tower_api_patch('inventories', curr_id=inv_id, payload=payload)
        return result

    # Tower inventory API PUT
    def inventory_put_update(self, inv_id, payload):
        result = self.tower_api_put_update('inventories', curr_id=inv_id, payload=payload)
        return result
