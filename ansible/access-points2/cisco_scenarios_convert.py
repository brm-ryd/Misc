#incomplete
import yaml
import re
SCENARIO_FILE="scenarios/all.txt"
GROUP_VAR_FILE="group_vars/all.yml"

class ScenarioParser(object):

    def __init__(self):
        self.rc = 0
        self.storage = dict()
        self.file_content = dict()

    def open(self):
        try:
            with open(GROUP_VAR_FILE, 'r') as fileObj:
                self.file_content=yaml.load(fileObj)
        except:
            open(GROUP_VAR_FILE, 'w').close()

    def read(self):
        scenario_number = 0
        scenario_step = 0
        scenario_name = ''
        name_pattern = re.compile(r'^(\d+)\.?\s+(.*)')
        step_pattern = re.compile(r'.*[])
