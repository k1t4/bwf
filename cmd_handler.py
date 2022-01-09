"""
Module that parses, validates and passes commands to core module for execution
"""
import core
from exceptions import ActionNotSpecified, TargetNotSpecified, TooManyArgs,\
    InvalidTarget, InvalidArgNum

allowed_actions = (
    'get',
    'create',
    'delete',
)

allowed_targets = {
    'get': ('username', 'password', 'credentials'),
    'create': ('username', 'password', 'credentials',),
    'delete': ()
}

# Combinations of command: strs:
# GET:
# - get credentials <smth>: prints username and password for items with <smth>
#                           in their name
# - get credentials: prints username and password for all items in vault
# - get username <smth>: prints username for items with <smth> in their name
# - get password <smth>: as previous but with password
#
# CREATE:
# - create credentials <item_name> <username> <password>
# - create username <item_name> <username>
# - create password <item_name> <password>
#
# DELETE:
# - delete <item_name>


def parse(input_str):
    """Performs initial parsing and validation and invokes
    specific parser function"""
    if not input_str:
        raise ActionNotSpecified
    action, *rest_args = input_str.split()

    if not rest_args:
        raise TargetNotSpecified

    if action == 'get':
        return get_action_parse(rest_args)
    if action == 'create':
        return create_action_parse(rest_args)
    if action == 'delete':
        return delete_action_parse(rest_args)


def get_action_parse(rest_args):
    if not rest_args:
        raise TargetNotSpecified
    target, *rest_args = rest_args
    if target not in allowed_targets['get']:
        raise InvalidTarget
    if target == 'credentials':
        if not rest_args:
            return core.get(target)
    search_name, *rest_args = rest_args
    if rest_args:
        raise TooManyArgs
    return core.get(target, search_name)


def create_action_parse(rest_args):
    if not rest_args:
        raise TargetNotSpecified
    target, *rest_args = rest_args
    if target not in allowed_targets['create']:
        raise InvalidTarget
    if target == 'credentials':
        if len(rest_args) != 3:
            raise InvalidArgNum
        return core.create(target, *rest_args)
    uname_or_pass, *rest_args = rest_args
    if rest_args:
        raise TooManyArgs
    return core.create(target, uname_or_pass)


def delete_action_parse(rest_args):
    if not rest_args:
        raise TargetNotSpecified
    target, *rest_args = rest_args
    if target not in allowed_targets['delete']:
        raise InvalidTarget
    if rest_args:
        raise TooManyArgs
    return core.delete(target)
