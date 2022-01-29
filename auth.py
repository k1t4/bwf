"""
Functions that are used for authentication
"""

import getpass
import json
import os
import re
import subprocess as sp


def is_user_logged_in() -> bool:
    """Checks if a user is logged-in or not"""
    completed_ps = sp.run(['bw', 'status'], capture_output=True)
    status = json.loads(completed_ps.stdout)['status']
    return status != 'unauthenticated'


def is_vault_locked():
    """Checks if vault of logged-in user is locked or not"""
    completed_ps = sp.run(['bw', 'status'], capture_output=True)
    status = json.loads(completed_ps.stdout)['status']
    return status == 'locked'


def unlock_and_get_token() -> str:
    """Gets user's session token"""
    print('Please, submit your password:')
    passwd = getpass.getpass('Password: ')
    completed_ps = sp.run(['bw', 'unlock', passwd], capture_output=True)
    # check for errors
    if completed_ps.returncode == 1:
        print('Incorrect password, try again...')
        return unlock_and_get_token()
    token = re.findall(r'BW_SESSION="(\S+)"', str(completed_ps.stdout))[0]
    return token


def export_token(token) -> None:
    """Exports user token to environment"""
    os.environ['BW_SESSION'] = token


def log_in_and_get_token() -> str:
    """
    Logs user in and returns session token to environment,
    should be called only if user is not logged-in
    """
    print('Please log-in')
    email = input('E-mail: ')
    passwd = getpass.getpass('Password: ')
    # need to ensure that it is safe
    completed_ps = sp.run(['bw', 'login', email, passwd], capture_output=True)
    if completed_ps.returncode == 1:
        print('Incorrect credentials, try again...', end='\n\n')
        return log_in_and_get_token()
    token = re.findall(r'BW_SESSION="(\S+)"', str(completed_ps.stdout))[0]
    print('You are successfully logged-in')
    return token


def log_user_out():
    """Logs user out"""
    sp.run(['bw', 'logout'], stdout=sp.DEVNULL)


def authenticate():
    """
    Authenticates user, unlocks the vault and exports session token
    """
    if not is_user_logged_in():
        token = log_in_and_get_token()
        export_token(token)
    elif is_vault_locked():
        token = unlock_and_get_token()
        export_token(token)

