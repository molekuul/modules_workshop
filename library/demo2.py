#!/usr/bin/python

# Import necessary libraries
from ansible.module_utils.basic import AnsibleModule

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
    result = {}
    touch = module.get_bin_path("touch")
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
    result = {}
    rm = module.get_bin_path("rm")
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
