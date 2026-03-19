# ansible-role-base

[![Lint](https://github.com/mikinhas/ansible-role-base/actions/workflows/lint.yml/badge.svg)](https://github.com/mikinhas/ansible-role-base/actions/workflows/lint.yml)

Ansible role for base system configuration on Ubuntu servers.

## Installation

```bash
ansible-galaxy role install mikinhas.base
```

## Features

- System packages update, upgrade and installation
- Automatic security updates (unattended-upgrades)
- SSH hardening (modern ciphers, key-only authentication)
- Fail2ban with SSH jail
- UFW firewall (deny incoming by default)
- Timezone and NTP configuration

## Supported Platforms

- Ubuntu 24.04 (Noble)

## Role Variables

### Packages

| Variable | Default | Description |
| --- | --- | --- |
| `base_packages` | `[vim]` | Base packages to install |
| `base_extra_packages` | `[]` | Additional packages to install |

### Unattended Upgrades

| Variable | Default | Description |
| --- | --- | --- |
| `base_unattended_upgrades` | `true` | Enable automatic security updates |
| `base_unattended_upgrades_autoreboot` | `false` | Enable automatic reboot after updates |
| `base_unattended_upgrades_autoreboot_time` | `"02:00"` | Reboot time if autoreboot is enabled |

### SSH Hardening

| Variable | Default | Description |
| --- | --- | --- |
| `base_ssh_hardening` | `true` | Enable SSH hardening |
| `base_ssh_port` | `22` | SSH port |
| `base_ssh_permit_root_login` | `"yes"` | Allow root login |
| `base_ssh_password_authentication` | `false` | Allow password authentication |
| `base_ssh_max_auth_tries` | `3` | Max authentication attempts |
| `base_ssh_kex_algorithms` | See `defaults/main.yml` | Key exchange algorithms |
| `base_ssh_ciphers` | See `defaults/main.yml` | Ciphers |
| `base_ssh_macs` | See `defaults/main.yml` | MAC algorithms |
| `base_ssh_host_key_algorithms` | See `defaults/main.yml` | Host key algorithms |

### Fail2ban

| Variable | Default | Description |
| --- | --- | --- |
| `base_fail2ban` | `true` | Enable fail2ban |
| `base_fail2ban_maxretry` | `5` | Max attempts before ban |
| `base_fail2ban_findtime` | `600` | Detection window in seconds (10min) |
| `base_fail2ban_bantime` | `86400` | Ban duration in seconds (24h) |

### UFW

| Variable | Default | Description |
| --- | --- | --- |
| `base_ufw` | `true` | Enable UFW firewall |
| `base_ufw_extra_rules` | `[]` | Additional firewall rules |

### Timezone

| Variable | Default | Description |
| --- | --- | --- |
| `base_timezone` | `"Europe/Paris"` | Server timezone |

## Usage

```yaml
- hosts: servers
  roles:
    - role: mikinhas.base
      vars:
        base_timezone: "Europe/Paris"
        base_extra_packages:
          - htop
          - curl
          - jq
        base_ssh_port: 2222
        base_fail2ban_maxretry: 3
        base_ufw_extra_rules:
          - port: 80
            proto: tcp
            comment: HTTP
          - port: 443
            proto: tcp
            comment: HTTPS
```

## Tags

Each feature can be run independently using tags:

```bash
ansible-playbook playbook.yml --tags ssh
ansible-playbook playbook.yml --tags fail2ban
ansible-playbook playbook.yml --tags ufw
```

Available tags: `packages`, `unattended-upgrades`, `ssh`, `fail2ban`, `ufw`, `timezone`

## Testing

Tests are run using Molecule with Vagrant (VirtualBox):

```bash
molecule test
```

## License

MIT

## Author

[mikinhas](https://github.com/mikinhas)
