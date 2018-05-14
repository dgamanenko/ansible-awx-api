from tower import AnsibleTower
from secrets import AnsibleTowerGetSecrets

class AnsibleTowerLaunchJob(AnsibleTower):
    def __init__(self, scope='write', tokens_file='secret_keys', run_from='remote'):
        secrets = AnsibleTowerGetSecrets(tokens_file=tokens_file, run_from=run_from, scope=scope).get_secrets()
        super(AnsibleTowerLaunchJob, self).__init__(host=secrets['awx_host'], token=secrets['awx_token'], schema=secrets['awx_schema'])

    # Launch tower job_template
    def launch_job_template(self, jt_id):
        url_path_rpart = 'job_templates'
        response = self.tower_api_post(url_path_rpart=url_path_rpart+'/{}'.format(jt_id) +'/'+'launch')
        return response

    # Launch tower workflow_job_template
    def launch_workflow_job_template(self, wjt_id):
        url_path_rpart = 'workflow_job_templates'
        response = self.tower_api_post(url_path_rpart=url_path_rpart+'/{}'.format(wjt_id) +'/'+'launch')
        return response
