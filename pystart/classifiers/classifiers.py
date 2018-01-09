def get_classifier_file():
    import os
    path = os.path.abspath(__file__)
    return os.path.join(os.path.dirname(path), 'classifiers.txt')


CLASSIFIERS = open(get_classifier_file()).read().strip().split("\n")

_prefix = "Operating System :: "
PLATFORMS = [p for p in CLASSIFIERS if p.startswith(_prefix)]
PLATFORMS = [p[len(_prefix):] for p in PLATFORMS]
