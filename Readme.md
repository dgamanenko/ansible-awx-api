
Ansible AWX API
================
Quick start to create STAGE deployment in AWX
------------------------------------
```
mv secret_keys.example secret_keys
edit tokens in secret_keys
virtualenv venv
pip install -r requirements.txt
source venv/bin/activate
```

```python
#!/usr/bin/python

from merge_yaml import MergeYAMLS
from get import AnsibleTowerGetData
from launch import AnsibleTowerLaunchJob
from update import AnsibleTowerUpdateData
from create import AnsibleTowerCreateData

def main():

    org_name = "RaccoonGang"
    project_name = "Example"

    awx_create = AnsibleTowerCreateData()
    ##Create inventory
    inv_pl = {"name": "{} STAGE", "description".format(project_name): "{} STAGE RG KVM".format(project_name), "organization": org_name, "variables": ""}
    inv_data = awx_create.inventory_post(inv_pl)

    inv_id = inv_data['id']

    ##Create inventory host
    inventory_variables: "example_var: 123\nexample_var2: 345"

    inv_host_pl = {"name": "127.0.0.1", "description": "{} STAGE RG KVM".format(project_name), "enabled": "true", "variables": inventory_variables}
    inv_host_data = awx_create.inventory_host_post(inv_id, inv_host_pl)

    ##Create project
    prj_pl = {"name": "configuration-example-stage","description": "OpenEdx RaccoonGang Ginkgo","scm_type": "git","scm_url": "https://github.com/raccoongang/configuration.git","scm_branch": "ginkgo-rg","scm_clean": "true","scm_delete_on_update": "true","organization": org_name,"scm_update_on_launch": "true"}
    prj_data = awx_create.project_post(payload=prj_pl)
    prj_id = prj_data['id']

    awx_get = AnsibleTowerGetData()
    ##Get inventory by id
    cred_id = awx_get.credentials_id_by_name(cred_name='Credential name')

    ##Create job_template
    jt_pl = {"name": "{} STAGE edx-platform", "description".format(project_name): "{} STAGE edx-platform KVM stage".format(project_name), "job_type": "run", "inventory": inv_id, "project": prj_id, "playbook": "playbooks/edx_single.yml", "skip_tags": "to-remove", "credential": cred_id}
    jt_data = awx_create.job_template_post(payload=jt_pl)
    jt_id = jt_data['id']

    ##Create job_template with labels
    jt_pl = {"name": "{} STAGE edx-platform", "description".format(project_name): "{} STAGE edx-platform KVM stage".format(project_name), "job_type": "run", "inventory": inv_id, "project": prj_id, "playbook": "playbooks/edx_single.yml", "skip_tags": "to-remove", "credential": cred_id}
    jt_lbl_pl = [{"name": "EDX", "organization": org_name}, {"name": "STAGE", "organization": org_name}, {"name": "KVM", "organization": org_name}]
    jt_data = awx_create.job_template_post(payload=jt_pl, labels_payload=jt_lbl_pl)
    jt_id = jt_data['id']

    awx_run = AnsibleTowerLaunchJob()
    ##Launch job_template
    data = awx_run.launch_job_template(jt_id=jt_id)

if __name__ == "__main__":
    main()

```

Usage:
------------------------------------
```python
org_name = "RaccoonGang"

#Get##########################
awx_get = AnsibleTowerGetData()

##Get all workflow_job_templates
wjt = awx_get.workflow_job_templates()

##Get workflow_job_template by id
wjt_by_id = awx_get.workflow_job_templates(wjt_id='152')

##Get extra_vars for all workflow_job_templates
wjt_extra_vars = awx_get.workflow_job_templates_extra_vars()

##Get extra_vars for all workflow_job_template by id
wjt_extra_vars_by_id = awx_get.workflow_job_templates_extra_vars(wjt_id='152')

##Get extra_vars hexdigest for all workflow_job_templates
wjt_extra_vars_hd = awx_get.workflow_job_templates_extra_vars(hexdigest = True)

##Get extra_vars hexdigest for workflow_job_template by id
wjt_extra_vars_hd_by_id = awx_get.workflow_job_templates_extra_vars(hexdigest = True)

##Get extra_vars for all job_templates
jt_extra_vars = awx_get.job_templates_extra_vars()

##Get extra_vars for all job_templates
jt_extra_vars_by_id = awx_get.job_templates_extra_vars(jt_id='123')

##Get extra_vars hexdigest for all job_templates
jt_extra_vars_hd = awx_get.job_templates_extra_vars(hexdigest = True)

##Get extra_vars hexdigest for job_templates by id
jt_extra_vars_hd_by_id = awx_get.job_templates_extra_vars(jt_id='123', hexdigest = True)

##Get all organizations
org = awx_get.organizations()

##Get organization by id
org_by_id = awx_get.organizations(org_id='2')

##Get all projects
prj = awx_get.projects()

##Get project by id
prj_by_id = awx_get.projects(project_id='123')

##Get all inventories
inv =  awx_get.inventories()

##Get inventory by id
inv =  awx_get.inventories(inv_id='123')

##Get variables for all inventories
inv_extra_vars = awx_get.inventories_variables()

##Get variables for inventory by id
inv_extra_vars_by_id = awx_get.inventories_variables(inv_id='123')

##Get variables hexdigest for all inventories
inv_extra_vars_hd = awx_get.inventories_variables(hexdigest = True)

##Get variables hexdigest for inventory by id
inv_extra_vars_hd_by_id = awx_get.inventories_variables(inv_id='123', hexdigest = True)

#Update#######################
awx_update = AnsibleTowerUpdateData()

##Update job_template by id (API PATCH)
data = {"description": "New description for job_template 153"}
jt_patch = awx_update.job_template_patch_update(jt_id = '153', payload = data)

##Update job_template by id (API PUT)
data = {"description": "New description for job_template 153"}
jt_put = awx_update.job_template_put_update(jt_id = '153', payload = data)

##Update workflow_job_template by id (API PATCH)
data = {"description": "New description for workflow_job_template 152"}
wjt_patch = awx_update.workflow_job_template_patch_update(wjt_id = '152', payload = data)

##Update workflow_job_template by id (API PUT)
data = {"description": "New description for workflow_job_template 152"}
wjt_put = awx_update.workflow_job_template_put_update(wjt_id = '152', payload = data)

##Update inventory by id (API PATCH)
data = {"description": "New description for inventory 123"}
inv_patch = awx_update.inventory_patch_update(inv_id = '123', payload = data)

##Update inventory by id (API PUT)
data = {"description": "New description for inventory 123"}
inv_put = awx_update.inventory_put_update(inv_id = '123', payload = data)

##Get merged context yaml files
###context_yaml_files from python dict
myaml = MergeYAMLS(context_yaml_files=['dev-test1.yml','dev-test2.yml'])
###recursively find all context_yaml_files in context_yaml_files_dir
myaml = MergeYAMLS(context_yaml_files_dir="./")
merged_yamls = myaml.merge_context_yaml_files()
awx_update = AnsibleTowerUpdateData()
data = {"description": "New description for inventory", "variables": merged_yamls}
inv_put = awx_update.inventory_patch_update(inv_id = '123', payload = data)

#Run##########################
awx_run = AnsibleTowerLaunchJob()
##Launch job_template
data = awx_run.launch_job_template(jt_id='153')

##Launch workflow_job_template
data = awx_run.launch_workflow_job_template(wjt_id='152')

#Create#######################
awx_create = AnsibleTowerCreateData()
##Create inventory
inv_pl = {"name": "example-inv", "description": "example-inv description", "organization": "RaccoonGang", "variables": "var: xxx"}
inv_data = awx_create.inventory_post(inv_pl)

##Create inventory host
inv_id = inv_data['id']
inv_host_pl = {"name": "127.0.0.1", "description": "example-inv-host", "enabled": "true", "variables": ""}
inv_host_data = awx_create.inventory_host_post(inv_id, inv_host_pl)

##Create credentials
creds_pl = {"name": "example-inv AWS", "description": "example-inv-Client AWS", "organization": "RaccoonGang", "credential_type": "Amazon Web Services", "inputs": {"username": "XXXXXXX","password": "YYYYYYYYYYYY"}}
creds_data = awx_create.credentials_post(creds_pl)

##Create ec2 inventory source
inv_id = inv_data['id']
inv_source_credential = "example-inv AWS"
inv_source_pl = {"name": "example-inv-source", "description": "example-inv-source", "source": "ec2", "source_vars": "", "credential": inv_source_credential, "source_regions": "ap-south-1", "instance_filters": "tag:awx-filter=edx-xxx-production", "overwrite": "true", "overwrite_vars": "true", "update_on_launch": "true"}
inv_source_data = awx_create.inventory_source_post(inv_id, inv_source_pl)

##Create job_template
jt_pl = {"name": "{} STAGE edx-platform", "description".format(project_name): "{} STAGE edx-platform KVM stage".format(project_name), "job_type": "run", "inventory": inv_id, "project": prj_id, "playbook": "playbooks/edx_single.yml", "skip_tags": "to-remove", "credential": cred_id}
jt_data = awx_create.job_template_post(payload=jt_pl)
jt_id = jt_data['id']

##Create job_template labels
jt_lbl_pl = {"name": "EDX", "organization": org_name}
jt_labels = awx_create.job_template_labels(jt_id=jt_id, payload=jt_lbl_pl)

##Create job_template with labels
jt_pl = {"name": "{} STAGE edx-platform", "description".format(project_name): "{} STAGE edx-platform KVM stage".format(project_name), "job_type": "run", "inventory": inv_id, "project": prj_id, "playbook": "playbooks/edx_single.yml", "skip_tags": "to-remove", "credential": cred_id}
jt_lbl_pl = [{"name": "EDX", "organization": org_name}, {"name": "STAGE", "organization": org_name}, {"name": "KVM", "organization": org_name}]
jt_data = awx_create.job_template_post(payload=jt_pl, labels_payload=jt_lbl_pl)
jt_id = jt_data['id']

##Create workflow_job_template
wjt_pl = {"name": "AWX_API_TEST", "description": "lalala", "extra_vars": "---\nVAR1: XXX\nVAR2: '{{x}}'", "organization": org_name, "ask_variables_on_launch": "false"}
wjt_data = awx_create.workflow_job_template_post(payload=wjt_pl)
wjt_id = wjt_data['id']

##Create workflow_job_template labels
jt_lbl_pl = {"name": "EDX", "organization": org_name}
wjt_labels = awx_create.workflow_job_template_labels(wjt_id=wjt_id, payload=jt_lbl_pl)

##Create workflow_job_template with labels
wjt_pl = {"name": "AWX_API_TEST", "description": "lalala", "extra_vars": "---\nVAR1: XXX\nVAR2: '{{x}}'", "organization": org_name, "ask_variables_on_launch": "false"}
wjt_lbl_pl = [{"name": "EDX", "organization": org_name}, {"name": "STAGE", "organization": org_name}, {"name": "KVM", "organization": org_name}]
wjt_data = awx_create.workflow_job_template_post(payload=wjt_pl, labels_payload=wjt_lbl_pl)
wjt_id = wjt_data['id']

```