def test_update_all_packages(host):
    check_return_false_in_changed_when_run_update_all_packages = host.ansible("apt", "upgrade=yes")["changed"]
    assert check_return_false_in_changed_when_run_update_all_packages == False

def test_vim_is_installed(host):
    nginx = host.package("vim")
    assert nginx.is_installed

def test_htop_is_installed(host):
    nginx = host.package("htop")
    assert nginx.is_installed

def test_fail2ban_is_installed(host):
    nginx = host.package("fail2ban")
    assert nginx.is_installed