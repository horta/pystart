from __future__ import absolute_import as _

import os
import datetime
from inquirer import prompt, Text, List, Checkbox
from .config import get_config_file
from .licenses import LICENSES
from .classifiers import PLATFORMS
from .changelog import get_changelog_content
from .manifest import get_manifest_content
from .readme import get_readme_content
from validate_email import validate_email
from .licenses import get_license_content
from .pip_search import pip_exact_search
from .username import get_full_name, get_email
import semantic_version

SETUP_PY_CONTENT = r"""from setuptools import setup

if __name__ == '__main__':
    setup()
"""

INIT_CONTENT = r"""from __future__ import absolute_import as _

__version__ = "{VERSION}"

__all__ = ["__version__"]
"""


def check_version(vrs):
    try:
        semantic_version.Version(vrs)
    except ValueError:
        return False
    return True


def is_pkgname_available(name):
    return not pip_exact_search(name)


class Project(object):
    def __init__(self):
        self._metadata = dict()
        self._cfg = ""

    def ask_questions(self):
        questions = [
            Text(
                'name',
                message="What's your package name",
                validate=lambda _, x: is_pkgname_available(x)),
            Text(
                'author',
                message="What's the name of package's author",
                default=get_full_name()),
            Text(
                'author_email',
                message="What's the e-mail of package's author",
                default=get_email(),
                validate=lambda _, x: validate_email(x)),
            Text('description', message="Brief description the package"),
            Text('keywords', message="Comma-delimited list of Keywords"),
            Text(
                'version',
                message="What's the initial version",
                default="0.1.0",
                validate=lambda _, x: check_version(x)),
            List(
                'license',
                message="What's the package license",
                choices=LICENSES,
                default="MIT"),
            Checkbox(
                'platforms',
                message="Select the platforms your package support",
                choices=PLATFORMS,
            )
        ]
        answers = prompt(questions)
        self._metadata.update(answers)

        keywords = self._metadata['keywords']
        keywords = [k.strip() for k in keywords.strip().split(',')]
        self._metadata['keywords'] = keywords

    def fill_default(self):
        self._metadata['maintainer'] = self._metadata['author']
        self._metadata['maintainer_email'] = self._metadata['author_email']
        download_url = 'https://github.com/project/package/releases/latest'
        self._metadata['download_url'] = download_url
        url = 'https://github.com/project/package'
        self._metadata['url'] = url

    def fill_cfg(self):
        cfg = get_config_file()
        cfg = cfg.replace("{NAME}", self._metadata["name"])
        cfg = cfg.replace("{AUTHOR}", self._metadata["author"])
        cfg = cfg.replace("{MAINTAINER}", self._metadata["author"])
        cfg = cfg.replace("{AUTHOR_EMAIL}", self._metadata["author_email"])
        cfg = cfg.replace("{MAINTAINER_EMAIL}", self._metadata["author_email"])
        cfg = cfg.replace("{DESCRIPTION}", self._metadata["description"])
        cfg = cfg.replace("{LICENSE}", self._metadata["license"])
        cfg = cfg.replace("{KEYWORDS}", ', '.join(self._metadata["keywords"]))
        cfg = cfg.replace("{PLATFORMS}",
                          ', '.join(self._metadata["platforms"]))
        self._cfg = cfg

    def _create_folders(self):
        name = self._metadata['name']
        os.mkdir(name)
        os.mkdir(os.path.join(name, name))

    def _create_init_file(self):
        name = self._metadata['name']
        version = self._metadata['version']

        with open(os.path.join(name, name, '__init__.py'), 'w') as f:
            content = INIT_CONTENT.replace("{VERSION}", version)
            f.write(content)

    def _create_setup_files(self):
        name = self._metadata['name']

        with open(os.path.join(name, 'setup.py'), 'w') as f:
            f.write(SETUP_PY_CONTENT)

        with open(os.path.join(name, 'setup.cfg'), 'w') as f:
            f.write(self._cfg)

    def _create_license_file(self):
        name = self._metadata['name']
        author = self._metadata['author']
        license = self._metadata['license']
        content = get_license_content(license)
        content = content.replace("<copyright holders>", author)
        year = str(datetime.datetime.now().year)
        content = content.replace("<year>", year)
        with open(os.path.join(name, 'LICENSE.md'), 'w') as f:
            f.write(content)

    def _create_changelog_file(self):
        name = self._metadata['name']
        version = self._metadata['version']
        description = self._metadata['description']
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        date = "{:4d}-{:02d}-{:02d}".format(year, month, day)
        content = get_changelog_content()
        content = content.replace("{NAME}", name)
        content = content.replace("{VERSION}", version)
        content = content.replace("{DATE}", date)
        content = content.replace("{DESCRIPTION}", description)
        with open(os.path.join(name, 'CHANGELOG.md'), 'w') as f:
            f.write(content)

    def _create_manifest_file(self):
        name = self._metadata['name']
        content = get_manifest_content()
        with open(os.path.join(name, 'MANIFEST.in'), 'w') as f:
            f.write(content)

    def _create_readme_file(self):
        name = self._metadata['name']
        description = self._metadata['description']
        license = self._metadata['license']
        content = get_readme_content()
        content = content.replace("{NAME}", name)
        content = content.replace("{DESCRIPTION}", description)
        content = content.replace("{LICENSE}", license)
        with open(os.path.join(name, 'README.md'), 'w') as f:
            f.write(content)

    def create_project(self):
        self._create_folders()
        self._create_init_file()
        self._create_setup_files()
        self._create_license_file()
        self._create_changelog_file()
        self._create_manifest_file()
        self._create_readme_file()


def entry_point():
    p = Project()

    p.ask_questions()
    p.fill_default()
    p.fill_cfg()
    p.create_project()
