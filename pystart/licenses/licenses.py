LICENSES = [
    'APACHEv2', 'GPLv2', 'BSD2CLAUSE', 'GPLv3', 'UNLICENSE', 'BSD3CLAUSE',
    'ISC', 'ZLIB', 'GG-GPL', 'MIT'
]


def get_license_content(license):
    import os
    path = os.path.abspath(__file__)
    fn = os.path.join(os.path.dirname(path), '{}-LICENSE.md'.format(license))
    return open(fn).read()
