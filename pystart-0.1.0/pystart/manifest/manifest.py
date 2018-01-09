def get_manifest_content():
    import os
    path = os.path.abspath(__file__)
    fn = os.path.join(os.path.dirname(path), 'MANIFEST.in.tpl')
    return open(fn).read()
