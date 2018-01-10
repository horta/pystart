from __future__ import unicode_literals as _

import os
import pwd
from subprocess import check_output, CalledProcessError


def get_full_name():
    return pwd.getpwuid(os.getuid())[4]


def get_email():
    try:
        cmd = "git config --global --get user.email 2>/dev/null"
        em = check_output(cmd, shell=True)
        em = em.decode('ascii')
        return em.strip()
    except CalledProcessError:
        return ""
