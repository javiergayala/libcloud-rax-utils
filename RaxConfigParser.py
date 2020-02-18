"""A module for parsing INI config files."""
import configparser
from dataclasses import dataclass


class RaxConfigParser:
    """Obtain RAX Public Cloud credentials from a PyRAX INI File."""

    def __init__(self, inifile=None):
        """Initialize the class.

        :param inifile: The INI file to parse
        :type path: str

        """
        self.inifile = inifile
        self.configparse = configparser.ConfigParser()
        self.loginInfo = self.parse_inifile()

    def parse_inifile(self):
        """Parse the config INI file.

        :returns: Login Credentials
        :rtype: LoginInfo

        """
        parsed_info = {
            "identity_type": None,
            "username": None,
            "api_key": None,
            "region": None,
        }
        res = self.configparse.read(self.inifile)
        for field in parsed_info.keys():
            try:
                parsed_info[field] = self.configparse["rackspace_cloud"][field]
            except KeyError:
                parsed_info[field] = None
                pass
        return LoginInfo(
            identity_type=parsed_info["identity_type"],
            username=parsed_info["username"],
            api_key=parsed_info["api_key"],
            region=parsed_info["region"],
        )

    def get_inifile(self):
        """Get the value used to instantiate the class.

        :returns: Path to the INI file
        :rtype: str

        """
        return self.inifile

    def __str__(self):
        """Present the class as a string."""
        return "inifile: " + self.inifile


@dataclass
class LoginInfo:
    """Class for keeping track of user login info.

    :param identity_type: Identity Type (should be "rackspace_cloud")
    :type identity_type: str
    :param username: Username for connecting to RAX Public Cloud
    :type username: str
    :param api_key: API Key to authenticate with
    :type api_key: str
    :param region: Region to connect to
    :type region: str
    """

    identity_type: str
    username: str
    api_key: str = None
    region: str = None
