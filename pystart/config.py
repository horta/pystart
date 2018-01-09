def get_config_file():
    import os
    path = os.path.abspath(__file__)
    f = os.path.join(os.path.dirname(path), 'setup.cfg.tpl')
    return open(f).read()
