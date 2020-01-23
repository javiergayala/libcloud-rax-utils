"""RAX wrapper class."""

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


class Rax(object):
    def __init__(self, *args, **kwargs):
        """Instantiate the Rax class and make a connection.

        Arguments:
            username {string} -- RAX username
            apikey {string} -- RAX API Key
            region {string} -- RAX Region
        """
        allowed_keys = set(["username", "apikey", "region"])
        self.__dict__.update((k, False) for k in allowed_keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        self.cls = get_driver(Provider.RACKSPACE)
        self.driver = self.cls(self.username, self.apikey, region=self.region)
        self.servers = []

    def get_servers(self):
        """Get a list of servers from the RAX API.

        Returns:
            {bool}} -- True if successful
        """
        self.servers = []
        self.servers += self.driver.list_nodes()
        return True

    def get_server(self, id=None):
        if not id:
            raise NameError
        self.get_servers()
        node = [node for node in self.servers if node.name == id]
        if len(node) == 1:
            return node[0]
        else:
            return node

    def print_servers(self):
        """Get and print the list of servers.

        Returns:
            {bool} -- True if successful, otherwise False
        """
        if self.get_servers():
            print(self.servers)
            return True
        else:
            return False

    def stop_server(self, node=None):
        if not node:
            raise NameError
        try:
            node.stop_node()
        except BaseHTTPError as identifier:
            return identifier
        return True

    def stop_servers(self, servers=[]):
        node_list = []
        for server in servers:
            node_list.append(self.get_server(server))
        for node in node_list:
            result = self.stop_server(node)
            if result:
                print("Node %s stopped." % node.name)
            else:
                print("Something went wacky with node %s: %s" % (node.name, result))
        return True
