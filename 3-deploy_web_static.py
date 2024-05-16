#!/usr/bin/python3
""" module to defin fabric file"""
from fabric.operations import local, run, put, env
from datetime import datetime
import os

env.hosts = ['18.233.67.128', '100.25.162.166']


def do_pack():
    """ Fabric script that generates a archive """
    try:
        local("sudo mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = "versions/web_static_{}.tgz".format(date)
        result = local("sudo tar -cvzf {} web_static".format(filename))
        if result.succeeded:
            return filename
    except Exception as error:
        return None


def do_deploy(archive_path):
    """
    distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        tar_filename = archive_path.split("/")[-1]
        filename = tar_filename.split(".")[0]
        run('sudo mkdir -p /data/web_static/releases/{}'.format(filename))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
            (tar_filename, filename))
        run('sudo rm -rf /tmp/{}'.format(tar_filename))
        run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(filename))
        return True
    except Exception as error:
        return False


def deploy():
    """ deploy all in one command"""
    path_to_tar = do_pack()

    if path_to_tar is None:
        return False
    result = do_deploy(path_to_tar)
    return result
