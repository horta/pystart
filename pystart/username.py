from __future__ import unicode_literals as _

import os
import pwd
from subprocess import check_output


def get_full_name():
    return pwd.getpwuid(os.getuid())[4]


def get_email():
    em = check_output("git config --global --get user.email", shell=True)
    em = em.decode('ascii')
    return em.strip()
