#!bin/python
# -*- encoding: utf-8 -*-

import docker
import os
import time

client = docker.from_env()

class DockerHandler(object):
    """Neuen Server anlegen
    
    Arguments:
        object {[type]} -- [description]
    """

    registry = {}
    client = None
    #Suche nach dem Verzeichnis Server
    home_dir = '%s/server' % os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
    home_dir = os.environ.get('BASE_PATH')

    def __init__(self):
        self.client = docker.from_env()
        # check if home_dir is ok and look for server2.py
        server_py = '%s/ServerAndClient/server/server2.py' % self.home_dir
        # if not os.path.exists(server_py):
        #     raise ValueError('%s does not exists' % server_py)
        self._refresh_registry()
        print(self.registry)
        return
        # make sure the db container is up and running
        # mit diesen Befehl könnte die Datenbank über das Termial erzeugt werden
        # docker run -d -e POSTGRES_USER=frank -e POSTGRES_PASSWORD=frank -e POSTGRES_DB=postgres --name dbserver -p 55432:5432 postgres
        if not self.registry.get('dbserver'):
            # not running, check if it exists
            dbserver = self.client.containers.list(all=True, filters={'name' : 'dbserver'})
            if dbserver:
                # Start des Servers falls gestoppt
                # container is stopped
                dbserver[0].restart()
            else:
                # Erzeugung des Postgres Servers
                ports_dic = {
                    '5432' : 55432
                }
                env_dic = {
                    'POSTGRES_USER' : 'frank',
                    'POSTGRES_PASSWORD' : 'frank',
                    'POSTGRES_DB' : 'postgres',
                }
                dbserver = client.containers.run(
                    'postgres',
                    name = 'dbserver',
                    auto_remove = False,
                    detach = True,
                    ports = ports_dic,
                    environment = env_dic
                )
                self.registry['dbserver'] = dbserver
                    
    def _refresh_registry(self, all=False):
        self.registry = {}
        for container in self.client.containers.list(all=all):
            name = container.name
            self.registry[name] = container
        
    def create_server(self, name, port):
        """
           docker run --name frank_server \
            --link dbserver:dbserver -p 40840:40840 opcua_server
        """
        self._refresh_registry(all=True)
        container = self.registry.get(name)

        if not container:
            links_dic = {
                'productionopcua_dbserver_1' : 'dbserver'
            }
            volumes_dic = {
                '%s/ServerAndClient/server' % self.home_dir :
                    {'bind': '/app', 'mode': 'ro'}
            }
            ports_dic = {
                '40840' : port
            }
            result = client.containers.run(
                'opcua_server',
                name = name,
                auto_remove = False,
                detach = True,
                links = links_dic,
                volumes = volumes_dic,
                ports = ports_dic,
                network = 'productionopcua_default',
            )
            self.registry[name] = result
            print(result.status)
            print(self.registry)
            return result.short_id
        else:
            # check if the container is running
            if container.status !='running':
                container.start()

    def remove_server(self, name):
        """
        remove a server from the database
        and delete the container
        """
        self._refresh_registry()
        container = self.registry.get(name)
        if container:
            # signal 15 informs the dbhandler within
            # the container to remove itself from
            # the database
            # and then exit
            container.kill(signal = 15)
            # now refresh the registry
            # name should not exist anymore
            time.sleep(1)
            self._refresh_registry()
            if self.registry.get(name):
                raise ValueError('Hoppala, should not happen')

    def signal_server(self, name):
        """
        remove a server from the database
        and delete the container
        """
        self._refresh_registry()
        container = self.registry.get(name)
        if container:
            # signal 14 informs the dbhandler within
            # the container to change its status
            container.kill(signal = 14)

    def list_servers(self, filter=[]):
        """list existing containers
        
        Keyword Arguments:
            filter {list} -- list of filter arguments (default: {[]})
        """
        print(self.registry.keys())


if __name__ == "__main__":
    handler = DockerHandler()
    s_id = handler.create_server('hugo', 40845)
    handler.list_servers()
    handler.remove_server('hugo')
    

