import argparse
import os
import sys


class ServerArgumentsParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser(description='Simple HipChat integration server',
                                                epilog="https://github.com/uPaid/hipchat-integration")

        self.__parser.add_argument("-p", "--port", metavar="PORT",
                                   type=int, default=80,
                                   dest="port",
                                   help="port the server should listen on")

        self.__parser.add_argument("-i", "--integrations", metavar="PATH",
                                   type=str, default=os.getcwd(),
                                   dest="integrations_path",
                                   help="path to the directory where integration scripts are located")

        self.__parser.add_argument("-t", "--tokens", metavar="TOKEN",
                                   nargs='+',
                                   dest="tokens",
                                   help="list of integration tokens in one of two possible formats: " +
                                        "GLOBAL_TOKEN_NAME:TOKEN or " +
                                        "ROOM:INTEGRATION_NAME:TOKEN")

        self.__parser.add_argument("-l", "--logfile", metavar="PATH",
                                   type=str, default=None,
                                   dest="logfile_path",
                                   help="path to the file that logs should be appended to")

        self.__args = self.__parser.parse_args()

        self.port = self.__args.port
        self.integrations_path = self.__args.integrations_path
        if not os.path.isdir(self.integrations_path):
            raise ValueError('"' + self.integrations_path + '" is not a valid directory')

        self.tokens = self.__args.tokens

        logfile_path = self.__args.logfile_path
        if logfile_path is not None:
            sys.stdout = sys.stderr = open(logfile_path, 'a')
