def test_update_all_packages(host):
    check_return_false_in_changed_when_run_update_all_packages = host.ansible("apt", "upgrade=yes")["changed"]
    assert check_return_false_in_changed_when_run_update_all_packages == False

def test_vim_is_installed(host):
    package = host.package("vim")
    assert package.is_installed

def test_htop_is_installed(host):
    package = host.package("htop")
    assert package.is_installed

def test_fail2ban_is_installed(host):
    package = host.package("fail2ban")
    assert package.is_installed
