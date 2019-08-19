import os
import json
import re
import pytest
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


"""
test package installation
"""


@pytest.mark.parametrize("name", [
    "nginx",
    "crontabs",
    "libselinux-python",
    "policycoreutils-python",
    "lbzip2-utils",
    "nginx",
    "openssl",
    "MySQL-python",
    "redis",
    "libreoffice",
    "jq",
    "mariadb-server",
    "php71w-fpm",
    "php71w-opcache",
    "php71w-common",
    "php71w-gd",
    "php71w-xml",
    "php71w-mbstring",
    "php71w-intl",
    "php71w-mcrypt",
    "php71w-mysql",
    "php71w-ldap",
    "php71w-imap",
    "php71w-pecl-apcu",
    "php71w-pecl-redis",
    "php71w-pecl-imagick",
    "php71w-process"
])
def test_package_installation(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


"""
test services (enabled / running)
"""


@pytest.mark.parametrize("name", [
    "mariadb",
    "redis",
    "nginx",
    "php-fpm"
])
def test_services(host, name):
    svc = host.service(name)
    assert svc.is_enabled
    assert svc.is_running


"""
test occ
"""


def test_occ(host):
    cmd = host.run_test("sudo -u nginx /var/www/nextcloud/occ")
    assert cmd.rc == 0


"""
test serverinfo
"""


def test_serverinfo(host):
    query = """ curl --user admin:test -H "Accept: application/json" \
                http://localhost/ocs/v2.php/apps/serverinfo/api/v1/info """
    cmd = host.run(query)
    res = json.loads(cmd.stdout)["ocs"]
    assert res["meta"]["status"] == "ok"
    assert res["data"]["nextcloud"]["system"]["memcache.local"] \
        == "\\OC\\Memcache\\APCu"
    assert res["data"]["nextcloud"]["system"]["memcache.locking"] \
        == "\\OC\\Memcache\\Redis"
    assert re.match('^nginx', res["data"]["server"]["webserver"])
    assert re.match('^7.1.', res["data"]["server"]["php"]["version"])
    assert res["data"]["server"]["database"]["type"] == "mysql"
