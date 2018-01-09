def get_changelog_content():
    import os
    path = os.path.abspath(__file__)
    fn = os.path.join(os.path.dirname(path), 'CHANGELOG.md.tpl')
    return open(fn).read()
