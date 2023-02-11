def test_vim_is_installed(host):
    nginx = host.package("vim")
    assert nginx.is_installed

def test_htop_is_installed(host):
    nginx = host.package("htop")
    assert nginx.is_installed

def test_fail2ban_is_installed(host):
    nginx = host.package("fail2ban")
    assert nginx.is_installed