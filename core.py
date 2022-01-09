"""
Core module where all commands are handled
"""
import shutil
import subprocess
import json


def get(target, *args):
    """Get action implementation"""
    # fetching fresh data
    subprocess.run(['bw', 'sync'])
    if target == 'credentials':
        if not args:
            completed_ps = subprocess.run(
                ['bw', 'list', 'items'], capture_output=True
            )
            return completed_ps.stdout
        search_pattern = args[0]
        completed_ps = subprocess.run(
            ['bw', 'list', 'items', '--search', search_pattern]
        )
        return completed_ps.stdout


def create(target):
    pass

def delete(target):
    pass

class Core:
    def __init__(self):
        ...

    @staticmethod
    def get(target, *args):
        completed_ps = subprocess.run(
            ['bw', 'list', 'items'], capture_output=True)
        items = json.loads(completed_ps.stdout)
        if target == 'password':
            pass
        elif target == 'login':
            bw_command = []
        elif target == 'creds':
            result = [(item['login']['username'], item['login']['password'])
                      for item in items if args[0] in item['name'].lower()]
            return result

    def create(self, target, *args):
        ...

    def delete(self, target, *args):
        ...

