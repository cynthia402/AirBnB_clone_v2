#!/usr/bin/python3
"""script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers
"""

from fabric.operations import run, put, env
import os

env.hosts = ['18.233.67.128', '100.25.162.166']


def do_deploy(archive_path):
    """
    distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return(False)
    try:
        put(archive_path, '/tmp/')
        tar_filename = archive_path.split("/")[-1]
        filename = tar_filename.split(".")[0]
        run('mkdir -p /data/web_static/releases/{}'.format(filename))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
            (tar_filename, filename))
        run('rm /tmp/{}'.format(tar_filename))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(filename))
        return(True)
    except Exception as error:
        return(False)
