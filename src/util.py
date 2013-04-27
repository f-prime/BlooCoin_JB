# -*- coding: utf-8 *-*
import os
import sys
import hashlib
import urllib2


def update(module_name):
    """
        Updates any module given its name.

        Arguments:
        module_name -- The __module__ member of an object.
    """
    module_name = get_name(module_name)
    url = 'https://raw.github.com/jBrown91/BlooCoin_JB/master/src/{0}'.format(
        module_name)
    local, remote = None, None
    with open(module_name, 'r') as f:
        local = hashlib.md5(f.read()).hexdigest()
    try:
        remote = urllib2.urlopen(url)
        remote = remote.read()
    except urllib2.HTTPError:
        return False
    if local != hashlib.md5(remote).hexdigest():
        with open(module_name, 'w') as f:
            f.write(remote)
        return True
    return False


def get_name(module):
    """Returns the filename of the given module."""
    name = sys.modules[module].__file__.split(os.sep)[-1]
    return name[:-1] if name[-1] == 'c' else name
