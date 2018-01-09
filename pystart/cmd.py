from __future__ import absolute_import as _

from inquirer import prompt, Text, List, Checkbox
from .config import get_config_file
from .licenses import LICENSES
from .classifiers import PLATFORMS
from .config import get_config_file
from validate_email import validate_email
from .pip_search import pip_exact_search


class InvalidConfigError(Exception):
    pass


class Project(object):
    def __init__(self):
        self._metadata = dict()

    def ask_questions(self):
        # questions = [
        #     Text('name', message="What's your package name"),
        #     Text('author', message="What's the name of package's author"),
        #     Text(
        #         'author_email',
        #         message="What's the e-mail of package's author",
        #         validate=lambda _, x: validate_email(x)),
        #     Text('description', message="Brief description the package"),
        #     Text('keywords', message="Comma-delimited list of Keywords"),
        #     List(
        #         'license',
        #         message="What's the package license",
        #         choices=LICENSES),
        #     Checkbox(
        #         'platforms',
        #         message="Select the platforms your package support",
        #         choices=PLATFORMS,
        #     )
        # ]
        # answers = prompt(questions)
        answers = dict(
            name="pystart",
            author="Danilo Horta",
            author_email="danilo.horta@gmail.com",
            description="Breif description",
            license="MIT",
            platforms=["Win", "Linux"],
            keywords=["keyword 0", "keyword 1"])
        self._metadata.update(answers)

    def fill_default(self):
        self._metadata['maintainer'] = self._metadata['author']
        self._metadata['maintainer_email'] = self._metadata['author_email']
        download_url = 'https://github.com/project/package/releases/latest'
        self._metadata['download_url'] = download_url
        url = 'https://github.com/project/package'
        self._metadata['url'] = url

    def check_package_name_availability(self):
        name = self._metadata['name']
        found = pip_exact_search(name)
        if found:
            print("Package name <{}> has already been taken.".format(name))
            raise InvalidConfigError()

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
        print(cfg)


def entry_point():
    p = Project()

    try:
        p.ask_questions()
        p.fill_default()
        p.check_package_name_availability()
        p.fill_cfg()
    except InvalidConfigError:
        pass
