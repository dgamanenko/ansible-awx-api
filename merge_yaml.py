#!/usr/bin/python

import os
import os.path
import json
from ruamel import yaml

class MergeYAMLS(object):

    def __init__(self, context_yaml_files=[], result_yaml=None, context_yaml_files_dir=None):
        ''' Constructor for this class. '''
        self.context_yaml_files = context_yaml_files
        self.context_yaml_files_dir = context_yaml_files_dir
        self.result_yaml = result_yaml
        self.data = {}
        try:
            #Load the yaml files
            if self.context_yaml_files_dir:
                for dirpath, dirnames, filenames in os.walk(self.context_yaml_files_dir):
                    for filename in [f for f in filenames if f.endswith(".yml") or f.endswith(".yaml")]:
                        self.context_yaml_files.append(os.path.join(dirpath, filename))

            for filename in self.context_yaml_files:
                with open(filename) as fp:
                    current_data = yaml.load(fp, Loader=yaml.Loader)
                self.data.update(current_data)
                fp.close()

            if self.result_yaml:
                #create a new file with merged yaml
                yaml.dump(self.data,file(self.result_yaml, 'w'))

        except yaml.YAMLError as error:
            print('Unable to merge context yaml files {0}: {1} '. format(self.context_yaml_files, error))

    # Get merged context yaml files
    def merge_context_yaml_files(self):
        results = json.dumps(self.data)
        return results
