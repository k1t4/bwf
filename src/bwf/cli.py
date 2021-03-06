#!/usr/bin/python

"""
Main execution module, all actions are called from here
"""

import argparse
import signal
import shutil
import sys

import bwf.auth as auth
from bwf.core import Executor


# show, create, delete - are subcommands:
#
# show - lists usernames and passwords of items which names
# correspond to a search pattern (empty search pattern = all records):
#   usage:
#       show -p pattern - list only passwords
#       show -u pattern - list only usernames
#       show -p - lists all passwords
#       show -u - lists all usernames
#       show == show -up == show -u -p - lists all usernames and passwords
#
# create (interactive) - creates a new credentials record in your wallet:
#   usage:
#       create -p item_name - create only password record
#       create -u item_name - create only username record
#       create -u -p item_name == create -up item name - create full record
#
# delete (interactive) - removes a record from your wallet that corresponds
# to a search pattern (if multiple items match -> requests user to choose one):
#   usage:
#       delete item_name - deletes items


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help='run interactive session of bw',
                    action='store_true')

subparsers_group = parser.add_subparsers(dest='action_name')

parser_show = subparsers_group.add_parser('show', help="list credentials")
parser_show.add_argument('-p', '--password', help='list passwords only',
                         action='store_true')
parser_show.add_argument('-u', '--username', help='list usernames only',
                         action='store_true')
parser_show.add_argument('search_pattern', nargs='?', const=None,
                         help='name of an item')

parser_create = subparsers_group.add_parser('create',
                                            help="create new credentials")
parser_create.add_argument('-p', '--password',
                           help='create password-only record',
                           action='store_true')
parser_create.add_argument('-u', '--username',
                           help='create username only record',
                           action='store_true')
parser_create.add_argument('item_name', help='name of new item')

parser_delete = subparsers_group.add_parser('delete', help="delete credentials")
parser_delete.add_argument('search_pattern', help='name of item to delete')

subparsers_group.add_parser('logout', help="logs user out")


def main():
    """
    Main function that handles command execution or
    invokes interactive shell if -i option is triggered
    """
    # registering signal handler
    def interrupt_signal_handler(sig, frame):
        print('\nGood-bye')
        sys.exit()
    signal.signal(signal.SIGINT, interrupt_signal_handler)

    # checking if original bw-cli is installed
    bw_path = shutil.which('bw')
    if not bw_path:
        print('This program is a wrapper of Bitwarden CLI, so to use it - you'
              ' should install Bitwarden CLI:\n'
              'https://bitwarden.com/help/cli/#download-and-install')
        sys.exit(1)

    cl_args = parser.parse_args()

    if cl_args.interactive and cl_args.action_name:
        print('Interactive option and action argument '
              'can not be used together. Pls try again')
        return None

    if cl_args.interactive or not cl_args.action_name:
        auth.authenticate()
        start_interactive_session()
    else:
        # no need for an authentication when logging-out
        if cl_args.action_name != 'logout':
            auth.authenticate()
        ex = Executor(cl_args)
        ex.execute_command()
        ex.print_result()


def start_interactive_session():
    """Starts an interactive shell session"""
    # adding a new subcommand so user can exit from interactive-mode
    subparsers_group.add_parser('exit', help='exit an interactive cli')
    while True:
        command = input('>>> ')
        # filling argv with interactive shell arguments
        # so argparse can work with it
        sys.argv = [''] + command.split()
        cl_args = parser.parse_args()
        if cl_args.interactive:     # warning a user
            print('You are already in interactive cli')
            continue
        cl_args.interactive = True  # setting it explicitly
        if cl_args.action_name == 'exit':
            print('Good-bye')
            sys.exit()
        # session token may expire during the session, so checking it
        if auth.is_vault_locked():
            token = auth.unlock_and_get_token()
            auth.export_token(token)
        ex = Executor(cl_args)
        ex.execute_command()
        ex.print_result()


if __name__ == "__main__":
    main()
