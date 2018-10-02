#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Joris Weijters <joris.weijters@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
version_added: "2.7"
options:
  name:
    description:
    - Name of the file
    required: yes
  location:
    description:
    - Location of the file
    default: /tmp
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
    returned: always
    type: string
    sample: file /tmp/hello_world created
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


def create_file(module, full_path_name):
    # create file
    # uses touch to create a file
    rc = 0
    result = {}
    touch = module.get_bin_path("touch")
    if not module.check_mode:
        (rc, out, err) = module.run_command([touch, full_path_name])
    if rc == 0:
        result['changed'] = True
        result['msg'] = "file: " + full_path_name + " created"
    else:
        module.fail_json(
                msg="could not create " + full_path_name, rc=rc, err=err)
    return result


def remove_file(module, full_path_name):
    # remove file
    # uses rm to remove file
    rc = 0
    result = {}
    rm = module.get_bin_path("rm")
    if not module.check_mode:
        (rc, out, err) = module.run_command([rm, full_path_name])
    if rc == 0:
        result['changed'] = True
        result['msg'] = "file: " + full_path_name + " removed"
    else:
        module.fail_json(
                msg="could not remove " + full_path_name, rc=rc, err=err)
    return result


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            location=dict(type='str', default='/tmp'),
            state=dict(type='str', choices=['absent', 'present'],
                       default='present'),
        ),
        supports_check_mode=True,
    )

    result = {
        'msg': "",
        'changed': False
    }

    # check if file exists
    full_path_name = module.params['location'] + "/" + module.params['name']
    current_file = check_file(module, full_path_name)

    # if state is present and file does not exist create file
    # if state is present and file does exist do nothing
    # if state is absent and file does not exist do nothing
    # if state is absent and file does exist remove file

    if module.params['state'] == 'present':
        if (not current_file['exists']):
            result = create_file(module, full_path_name)
    else:
        if (current_file['exists']):
            result = remove_file(module, full_path_name)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
