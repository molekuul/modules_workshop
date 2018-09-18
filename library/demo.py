#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Joris Weijters <joris.weijters@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
author:
- Joris Weijters (@molekuul)
module: demo
short_description: demo module
description:
    - demo module for the Ansible meetup benelux
version_added: "2.6"
options:
  name:
    desciption:
    - Name of the file
    required: no
  location:
    description:
    - Location of the file
    required: yes
  state:
    description:
    - whether the file should be present or absent
    choices: [ absent, present ]
    default: present
    
notes:
  - puts a file at a specific location
  - this is just to demo the writing of modules
'''

EXAMPLES = '''
# Add a file 
- name: Add a file
  demo:
    name: "hello_world"
    location: /tmp

# remove a file
- name: remove file
  demo:
    name: "hello_world"
    location: /tmp
    state: absent
'''

RETURN = '''
msg:
    description: return message
    returned: changed
    type: string
    sample: file added
changed:
    description: whether the file add or removal has been changed
    returned: always
    type: boolean
    sample: true
'''



# Import necessary libraries
from ansible.module_utils.basic import AnsibleModule

# end import modules
# start defining the functions

def check_file(module, full_path_name):
    # check if file exists
    # uses ls to check if file exists
    # returns dictionary content is boolean exists:[ True, False ]
    existsdict = {'exists': False}
    ls = module.get_bin_path('ls')
    (rc, out, err) = module.run_command([ls, full_path_name])
    if rc == 0:
        existsdict.update({'exists': True})
    return existsdict


def create_file(module):
    # create file
    # uses touch tou create a file

def remove_file(module):
    # remove file
    # uses rm to remove file

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            location=dict(type='str', default='/tmp'),
            state=dict(type='str', choices=['absent', 'present' ], default='present'),
        ),
        support_check_mode=True,
    )

    result = { 
            'msg': "",
            'changed': False
    }

    # check if file exists
    full_path_name = module['location'] + "/" + module['name'] 
    current_file = check_file(module, full_path_name)

    # if state is present and file does not exist create file
    # if state is present and file does exist do nothing
    # if state is absent and file does not exist do nothing
    # if state is absent and file does exist remove file
            
    if module.params['state'] == 'present':
        if (not current_file['exists']):
            create_file(module, full_path_name)
    else:
        if ( current_file['exists']):
            remove_file(module, full_path_name)

    module.exit_json(**result)

if __name__ == '__main__':
    main()
