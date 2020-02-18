"""Read credentials from an INI file.

Returns:
    {obj} -- Object containing parsed credentials info
"""
import configparser
from dataclasses import dataclass


class RaxConfigParser:
    """Obtain RAX Public Cloud credentials from a PyRAX INI File."""

    def __init__(self, inifile=None):
        """Initialize the class.

        Keyword Arguments:
        inifile {str} -- Path to the INI file (default: {None})
        """
        self.inifile = inifile
        self.configparse = configparser.ConfigParser()
        self.loginInfo = self.parse_inifile()

    def parse_inifile(self):
        """Parse the config INI file.

        Returns:
            {obj} -- LoginInfo dataclass
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

        Returns:
            {str} -- Path to the INI file
        """
        return self.inifile

    def __str__(self):
        """Present the class as a string."""
        return "inifile: " + self.inifile


@dataclass
class LoginInfo:
    """Class for keeping track of user login info."""

    identity_type: str
    username: str
    api_key: str = None
    region: str = None
