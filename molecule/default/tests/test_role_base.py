import pytest

def test_update_all_packages(host):
    check_return_false_in_changed_when_run_update_all_packages = host.ansible("apt", "upgrade=yes")["changed"]
    assert check_return_false_in_changed_when_run_update_all_packages == False


@pytest.mark.parametrize("package_name", [
    "fail2ban",
    "htop",
    "net-tools",
    "vim",
])
def test_if_all_packages_are_installed(host, package_name):
    packages = host.package(package_name)
    assert packages.is_installed


def test_fail2ban_sshd_jail_configuration_file_exists(host):
    sshd_jail_configuration_file = host.file("/etc/fail2ban/jail.d/sshd.conf")
    assert sshd_jail_configuration_file.exists


def test_fail2ban_service(host):
    service = host.service("fail2ban")
    assert service.is_running
    assert service.is_enabled
