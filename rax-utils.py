#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from configparser import ConfigParser

from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from logzero import logger

from RaxCompute import RaxCompute
from RaxConfigParser import RaxConfigParser

# cls = get_driver(Provider.RACKSPACE)


def main(args):
    """ Main entry point of the app """
    logger.info("Entering main function")
    logger.debug(args)
    logger.debug("Retrieving credentials")
    creds = RaxConfigParser(inifile=("/Users/jayala/.pyrax.%s" % args.env))
    logger.debug(creds)
    logger.info("Attempting connection to RAX Cloud")
    rax = RaxCompute(
        username=creds.loginInfo.username,
        apikey=creds.loginInfo.api_key,
        region=args.env,
    )
    if args.list:
        rax.list_servers_status()
    if args.nodes:
        logger.debug("nodes: %s" % args.nodes)
        if (args.stop and not args.destroy) and args.force:
            logger.info("Stopping nodes: %s" % args.nodes)
            rax.stop_servers(servers=args.nodes)
        elif (args.stop and not args.destroy) and not args.force:
            logger.error("ERROR: MUST USE --force TO STOP NODES")
        elif (args.destroy and not args.stop) and args.force:
            logger.info("Destroying nodes: %s" % args.nodes)
            rax.destroy_servers(servers=args.nodes)
        elif (args.destroy and not args.stop) and not args.force:
            logger.error("ERROR: MUST USE --force TO DESTROY NODES")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("env", help="Environment identifier")

    # Optional argument flag which defaults to False
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Use this flag to force the action to occur",
    )

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-s",
        "--stop",
        action="store_true",
        default=False,
        help="Stop servers (requires use of -f)",
    )
    parser.add_argument(
        "-d",
        "--destroy",
        action="store_true",
        default=False,
        help="Destroy servers (requires use of -f)",
    )

    parser.add_argument(
        "-l", "--list", action="store_true", default=False, help="List servers",
    )

    parser.add_argument(
        "-n",
        "--nodes",
        nargs="*",
        help="List of nodes (servers) to perform actions on",
        required=False,
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
