__author__ = 'aub3'
from fabric.api import local,task,lcd
from fabric.state import env
import logging,time,datetime,os

ec2_AMI = ''
env.user = "ubuntu"
env.key_filename = "" # "~/.ssh/cornellaub3nca.pem" #
env.hosts = ["",]


@task
def build():
    local('docker build --build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S) -t computationalhealthcare .')


@task
def rm():
    try:
        local('docker stop $(docker ps -a -q)')
    except:
        pass
    try:
        local('docker rm $(docker ps -a -q)')
    except:
        pass
    local('docker images -q --filter "dangling=true" | xargs docker rmi')
    local('docker volume rm $(docker volume ls -qf dangling=true)')

@task
def start():
    local('docker run -p 127.0.0.1:8111:8000 -d -t computationalhealthcare')


@task
def shell():
    local('docker exec -u="root" -it $(docker ps -l -q) bash')


@task
def test():
    local('docker exec -u="root" -it $(docker ps -l -q)  fab test')


@task
def server():
    local('open http://127.0.0.1:8111')
    local('docker exec -u="root" -it $(docker ps -l -q)  bash start_server.sh')
