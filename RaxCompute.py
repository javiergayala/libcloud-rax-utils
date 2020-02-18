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
        """Get a particular server by id.

        Keyword Arguments:
            id {str} -- String representation of the node's ID (default: {None})

        Raises:
            NameError: Raised if no name is id (name) is provided

        Returns:
            {obj} -- Object containing node.
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

        Returns:
            {bool} -- True if successful, otherwise False
        """
        if self.get_servers():
            print(self.servers)
            return True
        else:
            return False

    def list_servers_status(self):
        """List a table of server statuses.

        Returns:
            {bool} -- True if successful
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

        Keyword Arguments:
            node {obj} -- Node object to operate on (default: {None})

        Raises:
            NameError: Node named is not present.

        Returns:
            {bool | error} -- True if successful, otherwise returned error
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

        Keyword Arguments:
            servers {list} -- Servers to perform the stop action on (default: {[]})

        Returns:
            {bool} -- True if successful
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

        Keyword Arguments:
            node {obj} -- Node object to operate on (default: {None})

        Raises:
            NameError: Node named is not present.

        Returns:
            {bool | error} -- True if successful, otherwise returned error
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

        Keyword Arguments:
            servers {list} -- Servers to perform the stop action on (default: {[]})

        Returns:
            {bool} -- True if successful
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
