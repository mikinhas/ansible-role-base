"""Testinfra tests for ansible-role-base."""

import pytest


def test_system_is_updated(host):
    """Verify that system packages are up to date."""
    result = host.ansible("apt", "upgrade=yes")
    assert result["changed"] is False


@pytest.mark.parametrize("package_name", [
    "vim",
    "htop",
    "net-tools",
])
def test_base_packages_are_installed(host, package_name):
    """Verify that base packages are installed."""
    package = host.package(package_name)
    assert package.is_installed


def test_fail2ban_is_installed(host):
    """Verify that fail2ban is installed."""
    package = host.package("fail2ban")
    assert package.is_installed


def test_fail2ban_service_is_running(host):
    """Verify that fail2ban service is running and enabled."""
    service = host.service("fail2ban")
    assert service.is_running
    assert service.is_enabled


def test_fail2ban_sshd_jail_file_exists(host):
    """Verify that the sshd jail configuration file exists."""
    jail_file = host.file("/etc/fail2ban/jail.d/sshd.conf")
    assert jail_file.exists
    assert jail_file.is_file
    assert jail_file.user == "root"
    assert jail_file.group == "root"
    assert jail_file.mode == 0o644


def test_fail2ban_sshd_jail_content(host):
    """Verify the content of the sshd jail configuration."""
    jail_file = host.file("/etc/fail2ban/jail.d/sshd.conf")
    content = jail_file.content_string

    assert "[sshd]" in content
    assert "enable  = true" in content
    assert "bantime = 86400" in content
    assert "backend = systemd" in content


def test_fail2ban_sshd_jail_is_active(host):
    """Verify that the sshd jail is active in fail2ban."""
    result = host.run("sudo fail2ban-client status sshd")
    assert result.rc == 0
    assert "sshd" in result.stdout
