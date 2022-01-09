"""
Functions that are used for authentication
"""

import subprocess
import getpass
import re
import json
import os


def is_user_logged_in() -> bool:
    """Checks if a user is logged-in or not"""
    completed_ps = subprocess.run(['bw', 'status'], capture_output=True)
    status = json.loads(completed_ps.stdout)['status']
    return status != 'unauthenticated'


def get_session_token() -> str:
    """Gets user's session token"""
    print('Please, submit your password:')
    passwd = getpass.getpass('Password: ')
    completed_ps = subprocess.run(
        ['bw', 'unlock', passwd], capture_output=True)
    # check for errors
    if completed_ps.returncode == 1:
        print('Incorrect password, try again...')
        get_session_token()
    token = re.findall(r'BW_SESSION="(\S+)"', str(completed_ps.stdout))[0]
    return token


def export_token(token) -> None:
    """Exports user token to environment"""
    os.environ['BW_SESSION'] = token


def remove_token():
    """Deletes token from environment"""


def log_user_in() -> str:
    """
    Logs user in and returns session token to environment,
    should be called only if user is not logged-in
    """
    print('Please log-in')
    email = input('E-mail: ')
    passwd = getpass.getpass('Password: ')
    # need to ensure that it is safe
    completed_ps = subprocess.run(
        ['bw', 'login', email, passwd], capture_output=True)
    if completed_ps.returncode == 1:
        print('Incorrect credentials, try again...', end='\n\n')
        log_user_in()
    else:
        token = re.findall(
            r'BW_SESSION="(\S+)"', str(completed_ps.stdout))[0]
        print('You are successfully logged-in')
        return token


def log_user_out():
    """Logs user out"""
