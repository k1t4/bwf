"""
Core module where all commands are handled
"""
import subprocess
import json
from collections import namedtuple


class Executor:
    """
    A core class, that executes commands by fetching or writing data from
    original bw-cli
    """
    def __init__(self, cl_args):
        self.action = cl_args.action_name
        self.result_list = None

        if self.action == 'show':
            self.search_pattern = cl_args.search_pattern
            self.show_pass = cl_args.password
            self.show_uname = cl_args.username

        elif self.action == 'create':
            self.item_name = cl_args.item_name
            self.set_pass = cl_args.password
            self.set_uname = cl_args.username

        elif self.action == 'delete':
            pass

    def execute_command(self):
        """Interface for actions execution"""
        # fetching fresh data
        subprocess.run(['bw', 'sync'], stdout=subprocess.DEVNULL)
        if self.action == 'show':
            self.execute_cmd_show()
        if self.action == 'create':
            self.execute_cmd_create()
        if self.action == 'delete':
            pass

    def execute_cmd_show(self):
        """Generates a list of items to show based on a search_pattern"""
        completed_ps = subprocess.run(
            ['bw', 'list', 'items'], capture_output=True
        )
        items = json.loads(completed_ps.stdout)
        CleanItem = namedtuple('CleanItem', 'name username password')
        clean_items = []
        for item in items:
            clean_item = CleanItem(item['name'],
                                   item['login']['username'],
                                   item['login']['password'])
            clean_items.append(clean_item)

        if self.search_pattern:
            clean_items = list(
                filter(lambda i: self.search_pattern.lower() in i.name.lower(),
                       clean_items))

        self.result_list = clean_items

    def execute_cmd_create(self):
        """Creates a new record with credentials in a vault"""
        pass

    def execute_cmd_delete(self):
        """Deletes existing record in a vault"""
        pass

    def pretty_print(self):
        """Prints result of an executed action"""
        if self.action == 'show':
            output_s = ''
            both_params = self.show_pass and self.show_uname
            no_params = not (self.show_pass or self.show_uname)
            if both_params or no_params:
                for item in self.result_list:
                    output_s += f'{item.name}:\n' \
                                f'username: {item.username}\n' \
                                f'password: {item.password}\n\n'
            elif self.show_uname:
                for item in self.result_list:
                    output_s += f'{item.name}:\n' \
                                f'username: {item.username}\n\n'
            else:
                for item in self.result_list:
                    output_s += f'{item.name}:\n' \
                                f'password: {item.password}\n\n'

            print(output_s)

