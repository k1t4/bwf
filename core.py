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
        self.result = None

        if self.action == 'show':
            self.search_pattern = cl_args.search_pattern
            self.param_show_pass = cl_args.password
            self.param_show_uname = cl_args.username

        elif self.action == 'create':
            self.item_name = cl_args.item_name
            self.param_set_pass = cl_args.password
            self.param_set_uname = cl_args.username

        elif self.action == 'delete':
            self.search_pattern = cl_args.search_pattern

    def execute_command(self):
        """Interface for actions execution"""
        sp.run(['bw', 'sync'], stdout=sp.DEVNULL)   # fetching fresh data
        if self.action == 'show':
            self.execute_cmd_show()
        elif self.action == 'create':
            self.execute_cmd_create()
        elif self.action == 'delete':
            self.execute_cmd_delete()

    def execute_cmd_show(self):
        """Generates a list of items to show based on a search_pattern"""
        items = self.__get_items_by_search_pattern(self.search_pattern)

        CleanItem = namedtuple('CleanItem', 'name username password')
        clean_items = [
            CleanItem(i['name'], i['login']['username'], i['login']['password'])
            for i in items]

        self.result = clean_items

    def execute_cmd_create(self):
        """Creates a new record with credentials in a vault"""
        # getting templates and filling them with credentials
        template_item = self.__get_template('item')
        template_item_login = self.__get_template('item.login')
        # no args == both args
        if not (self.param_set_pass or self.param_set_uname):
            self.param_set_pass, self.param_set_uname = True, True
        if self.param_set_uname:
            username = input('New username: ')
            template_item_login['username'] = username
        if self.param_set_pass:
            password = getpass.getpass('Password: ')
            template_item_login['password'] = password

        template_item['name'] = self.item_name
        template_item['login'] = template_item_login

        # encoding and sending filled templates to bw cli
        encoded_template = base64.b64encode(json.dumps(template_item).encode())
        creator_ps = sp.run(['bw', 'create', 'item'], input=encoded_template,
                            stdout=sp.DEVNULL)
        if creator_ps == 1:
            raise ChildProcessError('bw create has finished with an error')
        self.result = f'Created item {self.item_name}'

    def execute_cmd_delete(self):
        """Deletes existing record in a vault by search pattern"""
        items = self.__get_items_by_search_pattern(self.search_pattern)
        if not items:
            self.result = 'No matching items, nothing to delete'
            return None
        elif len(items) == 1:
            item_to_delete = items[0]
        else:   # when multiple items match
            print('Multiple items match your query,'
                  ' please choose one to delete:')
            for index, item in enumerate(items):
                print(f'{index+1}) {item["name"]} with id {item["id"]}')
            chosen_index = input('Type which one to delete (ex: 1): ')
            while not chosen_index.isnumeric() \
                    or not (1 <= int(chosen_index) <= len(items)):
                chosen_index = input('Please, choose from integers: ')
            chosen_index = int(chosen_index)
            item_to_delete = items[int(chosen_index)-1]

        deleter_ps = sp.run(['bw', 'delete', 'item', item_to_delete['id']],
                            stdout=sp.DEVNULL)
        if deleter_ps.returncode == 1:
            raise ChildProcessError('bw delete has finished with an error')
        self.result = f'Deleted item {item_to_delete["name"]}'

    def pretty_print(self):
        """Prints result of an executed action"""
        if self.action == 'show':
            output_s = ''
            # no params == all params
            if not (self.param_show_pass or self.param_show_uname):
                self.param_show_uname, self.param_show_pass = True, True

            for item in self.result:
                output_s += f'{item.name}:\n'
                if self.param_show_uname:
                    output_s += f'username: {item.username}\n'
                if self.param_show_pass:
                    output_s += f'password: {item.password}\n'
                output_s += '\n'

            print(output_s, end='')
        else:
            print(self.result)

    @staticmethod
    def __get_template(template_name):
        """Just gets a template from bw cli"""
        template_ps = sp.run(['bw', 'get', 'template', template_name],
                             capture_output=True)
        return json.loads(template_ps.stdout)

    @staticmethod
    def __get_items_by_search_pattern(search_pattern):
        """Gets list of items that matches search pattern"""
        completed_ps = sp.run(['bw', 'list', 'items'], capture_output=True)
        items = json.loads(completed_ps.stdout)
        if search_pattern:
            items = list(
                filter(
                    lambda i: search_pattern.lower() in i['name'].lower(),
                    items))
        return items
