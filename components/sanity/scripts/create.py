#!/bin/python

from os.path import join, dirname

import fabric.api

from cloudify import ctx


def upload_keypair(local_key_path):
    ctx.logger.info('Uploading key {0}...'.format(local_key_path))
    manager_remote_key_path = '/tmp/mng-key.pem'
    fabric.api.put(local_key_path,
                   manager_remote_key_path,
                   use_sudo=True)
    # Better to use the user from the same source as everything else, but that
    # requires import utils, which doesn't seem to be working, perhaps because
    # this is run using fabric with a task name where the others aren't.
    fabric.api.sudo('chown cfyuser {}'.format(manager_remote_key_path))

    ctx.instance.runtime_properties['manager_remote_key_path'] = \
        manager_remote_key_path
