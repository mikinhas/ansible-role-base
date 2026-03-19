"""Testinfra tests for ansible-role-base."""

import pytest


# Packages

def test_base_packages_are_installed(host):
    """Verify that base packages are installed."""
    package = host.package("vim")
    assert package.is_installed


# Unattended upgrades

def test_unattended_upgrades_is_installed(host):
    """Verify that unattended-upgrades is installed."""
    package = host.package("unattended-upgrades")
    assert package.is_installed


def test_unattended_upgrades_service_is_running(host):
    """Verify that unattended-upgrades service is running and enabled."""
    service = host.service("unattended-upgrades")
    assert service.is_running
    assert service.is_enabled


def test_unattended_upgrades_config_exists(host):
    """Verify that unattended-upgrades config files exist."""
    config = host.file("/etc/apt/apt.conf.d/50unattended-upgrades")
    assert config.exists
    assert config.is_file

    auto = host.file("/etc/apt/apt.conf.d/20auto-upgrades")
    assert auto.exists
    assert auto.is_file


# SSH hardening

def test_ssh_hardening_config_exists(host):
    """Verify that SSH hardening config exists."""
    config = host.file("/etc/ssh/sshd_config.d/99-hardening.conf")
    assert config.exists
    assert config.is_file
    assert config.user == "root"
    assert config.group == "root"
    assert config.mode == 0o600


def test_ssh_hardening_config_content(host):
    """Verify SSH hardening config content."""
    result = host.run("sudo cat /etc/ssh/sshd_config.d/99-hardening.conf")
    assert result.rc == 0
    content = result.stdout

    assert "PasswordAuthentication no" in content
    assert "PubkeyAuthentication yes" in content
    assert "PermitEmptyPasswords no" in content
    assert "X11Forwarding no" in content
    assert "MaxAuthTries 3" in content


def test_sshd_service_is_running(host):
    """Verify that sshd service is running."""
    service = host.service("ssh")
    assert service.is_running
    assert service.is_enabled


# Fail2ban

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
    assert "enabled = true" in content
    assert "bantime = 86400" in content
    assert "findtime = 600" in content
    assert "maxretry = 5" in content


def test_fail2ban_sshd_jail_is_active(host):
    """Verify that the sshd jail is active in fail2ban."""
    result = host.run("sudo fail2ban-client status sshd")
    assert result.rc == 0
    assert "sshd" in result.stdout


# UFW

def test_ufw_is_installed(host):
    """Verify that UFW is installed."""
    package = host.package("ufw")
    assert package.is_installed


def test_ufw_is_active(host):
    """Verify that UFW is active."""
    result = host.run("sudo ufw status")
    assert "Status: active" in result.stdout


def test_ufw_default_deny_incoming(host):
    """Verify that UFW default policy denies incoming traffic."""
    result = host.run("sudo ufw status verbose")
    assert "deny (incoming)" in result.stdout


def test_ufw_allows_ssh(host):
    """Verify that UFW allows SSH."""
    result = host.run("sudo ufw status")
    assert "22/tcp" in result.stdout


# Timezone

def test_timezone_is_set(host):
    """Verify that timezone is set correctly."""
    result = host.run("timedatectl show --property=Timezone --value")
    assert result.stdout.strip() == "Europe/Paris"


def test_timesyncd_is_running(host):
    """Verify that systemd-timesyncd is running."""
    service = host.service("systemd-timesyncd")
    assert service.is_running
    assert service.is_enabled
