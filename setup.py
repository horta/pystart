from setuptools import setup

if __name__ == '__main__':
    console_scripts = ["pystart = pystart.cmd:entry_point"]
    setup(entry_points=dict(console_scripts=console_scripts))
