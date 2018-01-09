def get_readme_content():
    import os
    path = os.path.abspath(__file__)
    fn = os.path.join(os.path.dirname(path), 'README.md.tpl')
    return open(fn).read()
