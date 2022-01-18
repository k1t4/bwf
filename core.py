"""
Core module where all commands are handled
"""
import subprocess as sp
import json
from collections import namedtuple
import getpass
import base64


class Executor:
    """
    A core class, that executes commands by fetching/writing data from/to
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
        sp.run(['bw', 'sync'], stdout=sp.DEVNULL)
        if self.action == 'show':
            self.execute_cmd_show()
        if self.action == 'create':
            self.execute_cmd_create()
        if self.action == 'delete':
            pass

    def execute_cmd_show(self):
        """Generates a list of items to show based on a search_pattern"""
        completed_ps = sp.run(['bw', 'list', 'items'], capture_output=True)
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
        # getting templates and filling them with credentials
        template_ps = sp.run(['bw', 'get', 'template', 'item'],
                             capture_output=True)
        template_item = json.loads(template_ps.stdout)
        template_ps = sp.run(['bw', 'get', 'template', 'item.login'],
                             capture_output=True)
        template_item_login = json.loads(template_ps.stdout)
        # both args are not set = both args are true
        if not (self.set_pass or self.set_uname):
            self.set_pass, self.set_uname = True, True
        if self.set_uname:
            username = input('New username: ')
            template_item_login['username'] = username
        if self.set_pass:
            password = getpass.getpass('Password: ')
            template_item_login['password'] = password

        template_item['name'] = self.item_name
        template_item['login'] = template_item_login

        # encoding and sending filled templates to bw creator
        encoded_template = base64.b64encode(json.dumps(template_item).encode())
        creator_ps = sp.run(['bw', 'create', 'item'], input=encoded_template,
                            stdout=sp.DEVNULL)
        if creator_ps == 1:
            raise ChildProcessError('bw create has finished with an error')
        print(f'Created item {self.item_name}')

    def execute_cmd_delete(self):
        """Deletes existing record in a vault"""
        pass

    def pretty_print(self):
        """Prints result of an executed action"""
        if self.action == 'show':
            output_s = ''
            # no params
            if not (self.show_pass or self.show_uname):
                self.show_uname = True
                self.show_pass = True

            for item in self.result_list:
                output_s += f'{item.name}:\n'
                if self.show_uname:
                    output_s += f'username: {item.username}\n'
                if self.show_pass:
                    output_s += f'password: {item.password}\n'
                output_s += '\n'

            print(output_s, end='')

