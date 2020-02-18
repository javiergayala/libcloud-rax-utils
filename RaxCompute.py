"""RaxCompute wrapper class."""

from libcloud.common.exceptions import BaseHTTPError
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from prettytable import PrettyTable

from RaxUtilities import prGreen, prRed


class RaxCompute(object):
    """Connects to RAX Public Cloud for manipulation of nodes."""

    def __init__(self, *args, **kwargs):
        """Instantiate the Rax class and make a connection.

        :param username: RAX Public Cloud username
        :type username: str
        :param apikey: API Key for RAX Public Cloud
        :type apikey: str
        :param region: RAX Public Cloud Region
        :type region: str

        """
        allowed_keys = set(["username", "apikey", "region"])
        self.__dict__.update((k, False) for k in allowed_keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        self.cls = get_driver(Provider.RACKSPACE)
        self.driver = self.cls(self.username, self.apikey, region=self.region)
        self.servers = []

    def get_servers(self):
        """Get a list of servers from the RAX API.

        :returns: True if successful
        :rtype: bool

        """
        self.servers = []
        self.servers += self.driver.list_nodes()
        return True

    def get_server(self, id=None):
        """Get a particular server by id.

        :param str id: ID of the node to retrieve
        :return: Node object requested
        :rtype: Node
        :raises NameError: if the id is blank

        """
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

        :returns: True if successful
        :rtype: bool

        """
        if self.get_servers():
            print(self.servers)
            return True
        else:
            return False

    def list_servers_status(self):
        """List a table of server statuses.

        :returns: True if successful
        :rtype: bool
        """
        if self.get_servers():
            x = PrettyTable()
            x.field_names = ["Name", "UUID", "Current State"]
            x.align["Name"] = "l"
            x.align["Current State"] = "l"
            for server in self.servers:
                if server.state == "running":
                    x.add_row([server.name, server.uuid, prGreen(server.state)])
                elif server.state == "stopped":
                    x.add_row([server.name, server.uuid, prRed(server.state)])
                else:
                    x.add_row([server.name, server.uuid, server.state])
            print(x)
        return True

    def __stop_server(self, node=None):
        """Stop a server.

        :param obj node: Node object to operate on
        :returns: True if successful
        :rtype: bool
        :raises NameError: if no node defined or present

        """
        if not node:
            raise NameError
        try:
            node.stop_node()
        except BaseHTTPError as identifier:
            return identifier
        return True

    def stop_servers(self, servers=[]):
        """Stop a group/list of servers.

        :param list servers: Servers to perform the stop action on
        :returns: True if successful
        :rtype: bool

        """
        node_list = []
        for server in servers:
            node_list.append(self.get_server(server))
        for node in node_list:
            result = self.__stop_server(node)
            if result:
                print(prGreen("Node %s stopped." % node.name))
            else:
                print(
                    prRed("Something went wacky with node %s: %s" % (node.name, result))
                )
        return True

    def __destroy_server(self, node=None):
        """Destroy a server.

        :param obj node: Node object to operate on
        :returns: True if successful
        :rtype: bool
        :raises NameError: if no node defined or present
        """
        if not node:
            raise NameError
        try:
            node.destroy()
        except BaseHTTPError as identifier:
            return identifier
        return True

    def destroy_servers(self, servers=[]):
        """Destroy a group/list of servers.

        :param list servers: Servers to perform the destroy action on
        :returns: True if successful
        :rtype: bool
        """
        node_list = []
        for server in servers:
            node_list.append(self.get_server(server))
        for node in node_list:
            result = self.__destroy_server(node)
            if result:
                print(prGreen("Node %s DESTROYED." % node.name))
            else:
                print(
                    prRed("Something went wacky with node %s: %s" % (node.name, result))
                )
        return True
