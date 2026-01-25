# ansible-role-base

[![Lint](https://github.com/mikinhas/ansible-role-base/actions/workflows/lint.yml/badge.svg)](https://github.com/mikinhas/ansible-role-base/actions/workflows/lint.yml)

Ansible role for base system configuration on Ubuntu servers.

## Installation

```bash
ansible-galaxy role install mikinhas.base
```

## Features

- System packages update and upgrade
- Base packages installation
- Fail2ban installation and SSH jail configuration

## Supported Platforms

- Ubuntu 24.04 (Noble)
- Ubuntu 22.04 (Jammy)

## Role Variables

| Variable                  | Default       | Description                         |
| ------------------------- | ------------- | ----------------------------------- |
| `base_packages`           | `[vim]`       | List of packages to install         |
| `base_install_fail2ban`   | `true`        | Enable fail2ban installation        |
| `base_fail2ban_bantime`   | `86400`       | Ban duration in seconds (24h)       |
| `base_fail2ban_findtime`  | `600`         | Detection window in seconds (10min) |
| `base_fail2ban_maxretry`  | `5`           | Max attempts before ban             |
| `base_jail_files`         | `[sshd.conf]` | Jail configuration files to deploy  |

## Usage

```yaml
- hosts: servers
  roles:
    - role: mikinhas.base
      vars:
        base_packages:
          - vim
          - htop
          - curl
        base_install_fail2ban: true
        base_fail2ban_bantime: 3600
        base_fail2ban_maxretry: 3
```

## Testing

Tests are run using Molecule with Vagrant (VirtualBox):

```bash
molecule test
```

## License

MIT

## Author

[mikinhas](https://github.com/mikinhas)
