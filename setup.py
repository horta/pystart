from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

if __name__ == '__main__':
    console_scripts = ["pystart = pystart.cmd:entry_point"]
    setup(
        entry_points=dict(console_scripts=console_scripts),
        long_description=long_description)
