#!/usr/bin/python3
##############################################################################

import sys

def query_yes_no(prompt, resp=False):
    if prompt is None:
        prompt = 'Confirm'
        
    while True:
        ans = input(prompt)
        if not ans:
            sys.exit()
            return resp
        elif ans not in ['y', 'yes', 'Y', 'Yes', 'YES', 'n', 'N', 'no', 'No', 'NO']:
            print('please enter y or n.')
            continue
        elif ans == 'y' or ans == 'Y':
            return True
        elif ans == 'n' or ans == 'N':
            sys.exit()
            return False
        else:
            sys.exit()
