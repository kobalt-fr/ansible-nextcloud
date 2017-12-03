import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_package(host):
    user_ini_file = '/opt/not-nextcloud/.user.ini'
    occ_file = '/opt/not-nextcloud/occ'
    user_ini = host.ansible('stat', 'path={}'.format(user_ini_file))
    occ = host.ansible('stat', 'path={}'.format(occ_file))
    assert user_ini['stat']['exists']
    assert occ['stat']['exists']
