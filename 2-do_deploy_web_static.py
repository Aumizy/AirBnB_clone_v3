#!/usr/bin/python3
"""
a fab script that generates a .tgz file from a folder and
distributes an archive to your web servers
"""
import os
from fabric.api import *
from datetime import datetime

env.hosts = ["34.224.94.130", "54.209.115.104"]
env.user = "ubuntu"


def do_pack():
    """ a function that clones the repo and pack contents into archive.tgz """

    local("mkdir -p versions")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    file = f"versions/web_static_{timestamp}.tgz"
    result = local(f"tar -cvzf {file} web_static", capture=True)
    return file


def do_deploy(archive_path):
    """ distributes an archive to your web servers """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        latest_release = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run(f"sudo mkdir -p {latest_release}")
        run(f"sudo tar -xzf {archived_file} -C {latest_release}/")
        run(f"sudo rm {archived_file}")
        run(f"sudo mv {latest_release}/web_static/* {latest_release}")
        run(f"sudo rm -rf {latest_release}/web_static")
        run(f"sudo rm -rf /data/web_static/current")
        run(f"sudo ln -s {latest_release} /data/web_static/current")

        print("New version deployed!")
        return True

    return False
